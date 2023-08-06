# SPDX-FileCopyrightText: 2023 Yann Büchau <nobodyinperson@posteo.de>
# SPDX-License-Identifier: GPL-3.0-or-later

# internal modules
import math
import copy
import argparse
import pickle
import operator
import time
import datetime
import io
import os
import sys
import re
import json
import subprocess
import logging
import functools
import itertools
import shlex
from contextlib import contextmanager

# internal modules
from hledger_utils.utils import (
    flatten,
    handle_keyboardinterrupt,
    handle_exception,
)
from hledger_utils.version import __version__

# external modules
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates
from cycler import cycler
import psutil
import numpy as np
import scipy.stats

import rich
from rich import print
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.pretty import Pretty
from rich.syntax import Syntax

console = Console(stderr=True)

logger = logging.getLogger("hledger plot")


@contextmanager
def nothing():
    yield


def str_to_str_mapping(s):
    if m := re.fullmatch(r"^(?P<old>.+?)\s*(?:[👉⮕→➡️]|->)+\s*(?P<new>.+)$", s):
        return m.groups()
    else:
        raise argparse.ArgumentTypeError(
            f"Format: 'OLDNAME -> NEWNAME', not {s!r}"
        )


def str_times_float_to_str_mapping(s):
    if m := re.fullmatch(
        r"^(?P<old>.+?)\s*([*·×✖️])\s*(?P<factor>(?:\d+(?:[,.]\d*))|(?:\d*[,.]\d+))\s*(?:[👉⮕→➡️]|->)+\s*(?P<new>.+)$",
        s,
    ):
        d = m.groupdict()
        return d["old"], float(d["factor"]), d["new"]
    else:
        raise argparse.ArgumentTypeError(
            f"Format: 'OLDNAME * FLOAT -> NEWNAME', not {s!r}"
        )


def regex_to_str_mapping(s):
    if m := re.fullmatch(
        r"^(?P<pattern>.+?)\s*(?:[👉⮕→➡️]|->)+\s*(?P<name>.+)$", s
    ):
        pattern, name = m.groups()
        try:
            return re.compile(pattern), name
        except Exception as e:
            raise argparse.ArgumentTypeError(
                f"{pattern!r} is not a valid regular expression: {e}"
            )
    else:
        raise argparse.ArgumentTypeError(
            f"Format: 'REGEX -> NEWNAME', not {s!r}"
        )


def regex_to_json_dict_mapping(s):
    if m := re.fullmatch(
        r"^(?P<pattern>.+?)\s*(?:[👉⮕→➡️]|->)+\s*(?P<json>.+)$", s
    ):
        pattern, jsonstr = m.groups()
        try:
            pattern = re.compile(pattern)
        except Exception as e:
            raise argparse.ArgumentTypeError(
                f"{pattern!r} is not a valid regular expression: {e}"
            )
        try:
            jsondict = json.loads(jsonstr)
        except json.JSONDecodeError as e:
            raise argparse.ArgumentTypeError(
                f"{jsonstr!r} is invalid JSON: {e}"
            )
        if not isinstance(jsondict, dict):
            raise argparse.ArgumentTypeError(
                f"{jsonstr!r} is not a JSON object/dict!"
            )
        return pattern, jsondict
    else:
        raise argparse.ArgumentTypeError(f"Format: 'REGEX -> JSON', not {s!r}")


def regex(s):
    try:
        pattern = re.compile(s)
    except Exception as e:
        raise argparse.ArgumentTypeError(
            f"{pattern!r} is not a valid regular expression: {e}"
        )
    return pattern


def regex_with_date_range_and_reference_date(s):
    fmt_example = "Format example: --trend '^costs:food  [2022-01-01:2022-05-31:7] @ 2022-02-01', not {s!r}"
    if m := re.search(
        r"^(?P<pattern>\S+)"
        r"(?:\s+\[(?P<range>(?P<start>[^\]:]*):(?P<end>[^\]:]*))(?::(?P<interval>\d*))?\])?"
        r"(?:\s+@\s*(?P<reference>\S+)\s*)?"
        r"$",
        s,
    ):
        d = m.groupdict()
        try:
            pattern = re.compile(d["pattern"])
        except Exception as e:
            raise argparse.ArgumentTypeError(
                f"{d['pattern']!r} is not a valid regular expression: {e}"
            )
        try:
            timerange = slice(
                None if pd.isna(t := pd.to_datetime(d["start"])) else t,
                None if pd.isna(t := pd.to_datetime(d["end"])) else t,
            )
        except Exception as e:
            raise argparse.ArgumentTypeError(
                f"{d['range']!r} is not a valid time range (error: {e}).\n{fmt_example}"
            )
        interval = handle_exception(None, int, d["interval"])
        try:
            reference = pd.to_datetime(d["reference"] or None)
        except Exception as e:
            raise argparse.ArgumentTypeError(
                f"{d['reference']!r} is not a valid time (error: {e}).\n{fmt_example}"
            )
        return pattern, timerange, interval, reference
    else:
        raise argparse.ArgumentTypeError(fmt_example)


def str_with_index_list(s):
    return [
        (m, handle_exception(None, int, i))
        for m, i in re.findall(r"([a-z]+)(?:\((\d+)\))?", s)
    ]


parser = argparse.ArgumentParser(
    description=f"""

📈  Plot hledger data, browse it interactively and save the graphs

Usage: Replace 'hledger' in your command with 'hledger-plot' or 'hledger plot --', for example:

hledger balance -M Costs
      ⮕  hledger plot -- balance -M Costs (double-dash after 'hledger plot')
      ⮕  hledger-plot    balance -M Costs (invoking hledger-plot directly, no double-dash)
      ⮕  hledger plot    balance -M Costs (only works without 'hledger-plot'-specific options)

version {__version__}, written by Yann Büchau, source code is at https://gitlab.com/nobodyinperson/hledger-utils
""".strip(),
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=f"""

ℹ️  Note
=======

- Currently, only plotting 'hledger balance ...' results is supporting.
  You can get quite close to 'hledger register ...' with 'hledger balance --daily' though.
- If you get weird errors like 'hledger: Error: Unknown flag XXXX', see above how to invoke hledger-plot
- If you instantly get an error like `/bin/sh: line 1: b: command not found` it probably means you need to do some escaping in your hledger query, especially the pipe character „|” and the asterisk „*”, like `hledger plot -- acct:'a\\|b' --trend '.\\*'`.

🤷 Examples
===========

# Fine-grained past and forecasted Assets
> hledger-plot balance --depth=2 --daily ^Assets: --historical --forecast --end 2030

# Monthly Cost overview with forecast
> hledger-plot balance --depth=2 --monthly ^Costs: --forecast --end 2030

# „How much did and will I pay for that one house?” (if you tagged house transactions with '; house: MyHouse')
> hledger-plot balance not:acct:^Assets --historical --daily tag:house=MyHouse --pivot=house --forecast --end 2030

version {__version__}, written by Yann Büchau, source code is at https://gitlab.com/nobodyinperson/hledger-utils
""".strip(),
)
parser.add_argument(
    "-V", "--version", action="version", version=f"%(prog)s {__version__}"
)
parser.add_argument(
    "-o",
    "--output",
    metavar="PATH",
    action="append",
    default=[],
    help="save plot to file (e.g. 'plot.pdf', 'plot.png', 'plot.fig.pickle', etc.). "
    "Can be specified multiple times.",
)
parser.add_argument(
    "--no-show", help="don't show the plot", action="store_true"
)
parser.add_argument(
    "--terminal",
    help="Plot in terminal (with drawilleplot)",
    action="store_true",
)
parser.add_argument(
    "-v",
    "--verbose",
    action="count",
    default=0,
    help="verbose output. More -v ⮕ more output",
)
parser.add_argument(
    "-q",
    "--quiet",
    action="count",
    default=0,
    help="less output. More -q ⮕ less output",
)


# styling
parser_styling_group = parser.add_argument_group(
    title="🎨  Styling", description="Options controlling the plot style"
)
parser_styling_group.add_argument("--title", help="window and figure title")
parser_styling_group.add_argument(
    "--axtitle", help="axes title. Defaults to hledger query."
)
parser_styling_group.add_argument(
    "--no-today", action="store_true", help="don't add a 'today' line"
)
parser_styling_group.add_argument(
    "--stacked", help="stacked bar chart", action="store_true"
)
parser_styling_group.add_argument(
    "--barplot",
    help="create a bar chart instead of lines",
    action="store_true",
)
parser_styling_group.add_argument(
    "--rcParams",
    metavar="JSON",
    action="append",
    help="""JSON rcParams (e.g. '{"figure.figsize":"10,10"}'). """
    "Can be specified multiple times. "
    "Later keys overwrite previous existing ones. "
    "See https://matplotlib.org/stable/tutorials/introductory/customizing.html for reference.",
    type=lambda x: json.loads(x),
    default=[],
)
parser_styling_group.add_argument(
    "--xkcd",
    action="store_true",
    help="XKCD mode (Install 'Humor Sans' / 'XKCD Font' for best results)",
)
parser_styling_group.add_argument(
    "--drawstyle",
    choices={"default", "steps-mid", "steps-pre", "steps-post", "steps"},
    help="drawstyle for line plots",
)
parser_styling_group.add_argument(
    "--style",
    metavar="REGEX -> JSON",
    action="append",
    type=regex_to_json_dict_mapping,
    help="""Mapping like 'REGEX -> JSON' to add extra styling arguments for columns, "
    "e.g. '^Cost: -> {"linewidth":5,"linestyle":"dashed"}'"""
    "Can be specified multiple times.",
    default=[],
)
parser_styling_group.add_argument(
    "--account-format",
    help="Format for account name including the currency. "
    "Default is '{account} ({commodity})' "
    "if there are multiple currencies, otherwise just '{account}'. "
    "Applied before any other modifications/matching.",
    default=None,
)


# modification
parser_modify_group = parser.add_argument_group(
    title="🔢  Data Modification",
    description="Options for manipulating the data",
)
parser_modify_group.add_argument(
    "--invert",
    metavar="REGEX",
    type=regex,
    help="patterns to invert amounts. Default is to invert all.",
    action="append",
    nargs="?",
    default=[],
)
parser_modify_group.add_argument(
    "--rename",
    metavar="OLDNAME -> NEWNAME",
    help="mapping(s) like 'OLD1 -> NEW1' for renaming columns. Can be specified multiple times.",
    action="append",
    type=str_to_str_mapping,
    default=[],
)
parser_modify_group.add_argument(
    "--sum",
    metavar="REGEX -> NEWNAME",
    type=regex_to_str_mapping,
    action="append",
    nargs="?",
    help="Mapping like 'REGEX -> NAME' to sum matching columns into a new field. "
    "Can be specified multiple times. "
    "Use e.g. --sum '.* -> total' to get a total value.",
    default=[],
)
parser_modify_group.add_argument(
    "--mean",
    metavar="REGEX -> NEWNAME",
    type=regex_to_str_mapping,
    action="append",
    nargs="?",
    help="Mapping like 'REGEX -> NAME' to average matching columns into a new field. "
    "Can be specified multiple times. ",
    default=[],
)
parser_modify_group.add_argument(
    "--multiply",
    metavar="NAME * FLOAT -> NEWNAME",
    type=str_times_float_to_str_mapping,
    action="append",
    help="Mapping like 'REGEX * FLOAT -> NAME' "
    "to multiply a column with a value "
    "and store it into a new column. "
    "Can be specified multiple times. ",
    default=[],
)
parser_modify_group.add_argument(
    "--resample",
    metavar="INTERVAL",
    action="append",
    help="DataFrame.resample() argument for data resampling "
    "(e.g. '60d' for a 60-day mean, "
    "see https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.resample.html)",
    default=[],
)
parser_modify_group.add_argument(
    "--drop",
    metavar="REGEX",
    help="regular expressions for dropping columns right before plotting. "
    "Can be specified multiple times.",
    action="append",
    type=regex,
    default=[],
)
parser_modify_group.add_argument(
    "--only",
    metavar="REGEX",
    help="regular expressions for keeping only matching columns for plotting. "
    "Can be specified multiple times.",
    action="append",
    type=regex,
    default=[],
)
parser_modify_group.add_argument(
    "--trend",
    metavar="REGEX [STARTDATE:ENDDATE:DAYS] @ REFERENCEDATE",
    help="Fit a linear trend line to columns matching the REGEX, "
    "optionally only using a specified date range as input. "
    "Example: '^costs:food [2022-01-01:2022-05-31:7] @ 2022-03-01' to fit a trend "
    "to the first half of 2022 and show the 7-day slope and the value at start of March in the legend. "
    "Whitespace in the REGEX is not allowed as a space is needed to separate it from the timerange. "
    "You may use a dot (.) instead in the pattern. "
    "You can leave the date range and the reference date out. If you specify a date range, "
    "you can leave start and/or end time out or specify 'today', but the colon (:) needs to stay. "
    "The interval is optional and defaults to 1. "
    "If you specify a reference date outside the given range, an extrapolation line will be added. "
    "Can be specified multiple times.",
    action="append",
    nargs="?",
    type=regex_with_date_range_and_reference_date,
    default=[],
)
parser_modify_group.add_argument(
    "--mod-order",
    metavar="LIST",
    default=str_with_index_list(
        default := "rename invert sum multiply resample mean trend drop only"
    ),
    help="List of modification steps like 'sum(1),rename(2),resample(1)' "
    "specifying the application order of modifiers. "
    "The indices refer to the Nth instruction of that type (1-based). "
    "Without an index, all modifiers of that type are executed in order. "
    f"Default order: {default!r}",
    type=str_with_index_list,
)


hledger_parser = argparse.ArgumentParser(prog="hledger")
hledger_parser.add_argument("--output-format", "-O")
hledger_parser.add_argument("--file", "-f")
# CAUTION: These options are handled differently across hledger versions!
hledger_parser.add_argument("--market", "--value", "-V", action="store_true")
# hledger commands
hledger_subparsers = hledger_parser.add_subparsers(
    required=True, dest="command"
)
hledger_balance_subparser = hledger_subparsers.add_parser(
    "balance", aliases=["b", "bal"]
)
hledger_balance_subparser.add_argument("--layout")
hledger_balance_subparser.add_argument(
    "--historical", "-H", action="store_true"
)
aggregation_period_args = [
    hledger_balance_subparser.add_argument(
        "--daily", "-D", action="store_true"
    ),
    hledger_balance_subparser.add_argument(
        "--weekly", "-W", action="store_true"
    ),
    hledger_balance_subparser.add_argument(
        "--monthly", "-M", action="store_true"
    ),
    hledger_balance_subparser.add_argument(
        "--quarterly", "-Q", action="store_true"
    ),
    hledger_balance_subparser.add_argument(
        "--yearly", "-Y", action="store_true"
    ),
]
aggregation_periods = tuple(
    map(operator.attrgetter("dest"), aggregation_period_args)
)
hledger_subparsers.add_parser("register", aliases=["r", "reg"])
hledger_subparsers.add_parser("print")
hledger_subparsers.add_parser("accounts", aliases=["a", "acc"])
hledger_subparsers.add_parser("prices")
hledger_subparsers.add_parser("stats")
hledger_subparsers.add_parser("tags")
hledger_subparsers.add_parser("web")


@handle_keyboardinterrupt(
    console=console,
    exitcode=handle_exception(
        0, int, os.environ.get("HLEDGER_PLOT_KEYBOARDINTERRUPT_EXITCODE")
    ),
)
def cli(cli_args=sys.argv[1:]):
    args, hledger_args = parser.parse_known_args()
    logging.basicConfig(
        level={
            -3: "CRITICAL",
            -2: "ERROR",
            -1: "WARNING",
            0: "INFO",
            1: "DEBUG",
        }.get(
            (v := args.verbose - args.quiet),
            logging.CRITICAL + abs(v) if v < -3 else "NOTSET",
        ),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True)],
    )
    for name in logging.root.manager.loggerDict:
        if "hledger" not in name:
            logging.getLogger(name).setLevel(10000)

    logger.debug(f"{args = }")
    if args.invert == [None]:
        args.invert = [re.compile(r".*")]
        logger.debug(
            f"Assuming you want to --invert all columns, "
            "setting patterns to {args.invert}"
        )
    if args.sum == [None]:
        args.sum = [(re.compile(r".*"), "∑ sum")]
        logger.debug(
            f"Assuming you want to --sum all columns, "
            "setting mapping to {args.sum}"
        )
    if args.mean == [None]:
        args.mean = [(re.compile(r".*"), "⌀ mean")]
        logger.debug(
            f"Assuming you want to --mean all columns, "
            "setting mapping to {args.mean}"
        )
    if args.trend == [None]:
        args.trend = [
            (
                re.compile(r".*"),
                slice(None, None, None),
                None,
                None,
            )
        ]
        logger.debug(
            f"Assuming you want to add a --trend for all columns, "
            "setting selector to {args.trend}"
        )
    logger.debug(f"{hledger_args = }")

    try:
        (
            hledger_parsed_args,
            hledger_unknown_args,
        ) = hledger_parser.parse_known_args(hledger_args)
    except BaseException as e:
        logger.warning(
            "Your hledger command {} looks broken".format(
                repr(" ".join(hledger_args))
            )
        )
        sys.exit(1)
    logger.debug(f"{hledger_parsed_args = }")
    logger.debug(f"{hledger_unknown_args = }")

    # TODO: automatically get aliases from above?
    parseable_hledger_commands = ["balance", "b", "bal"]
    if hledger_parsed_args.command not in parseable_hledger_commands:
        logger.info(
            "Currently, only the {} commands' output can be parsed and plotted".format(
                ",".join(map("'{}'".format, parseable_hledger_commands))
            )
        )
        sys.exit(1)

    hledger_executable = "hledger"
    hledger_parent_process = psutil.Process(os.getppid())
    if "hledger" in hledger_parent_process.cmdline()[0]:
        hledger_executable = hledger_parent_process.cmdline()[0]

    hledger_cmdline_parts = [hledger_executable] + hledger_args
    if hledger_parsed_args.output_format is None:
        hledger_cmdline_parts.append("-Ocsv")
    elif hledger_parsed_args.output_format != "csv":
        logger.info(
            "Please don't specify an output format for hledger other than csv"
        )
        sys.exit(1)

    hledger_cmdline_extra_args = []
    if "balance".startswith(hledger_parsed_args.command):
        if (layout := hledger_parsed_args.layout) and layout != "tidy":
            logger.error(
                "Please don't specify something else than --layout=tidy"
            )
            sys.exit(1)
        else:
            hledger_cmdline_extra_args.append("--layout=tidy")
        if not hledger_parsed_args.historical:
            logger.info(
                "ℹ️  Hint: You might want to consider adding --historical/-H to get the real balances at these times"
            )
        if not hledger_parsed_args.market and not any(
            "cur:" in arg for arg in hledger_unknown_args
        ):
            logger.info(
                "ℹ️  Hint: You might want to consider converting amounts to one currency via --market/--value/-V or selecting only one currency e.g. with 'cur:€'"
            )
        if not any(
            map(lambda x: getattr(hledger_parsed_args, x), aggregation_periods)
        ):
            logger.info("Adding --daily aggregation period for you")
            hledger_cmdline_extra_args.append("--daily")

    def hledger_to_dataframe(hledger_cmdline_parts):
        hledger_cmdline_parts.extend(hledger_cmdline_extra_args)
        hledger_cmdline = shlex.join(hledger_cmdline_parts)
        logger.info("🚀  Executing {}".format(repr(hledger_cmdline)))
        try:
            hledger = subprocess.Popen(
                hledger_cmdline_parts,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding="utf-8",
                errors="ignore",
            )
        except BaseException as e:
            logger.info(
                "Couldn't execute {}: {}".format(repr(hledger_cmdline), e)
            )
            sys.exit(1)

        # TODO: Reading the whole output at once is ridiculous.
        # WAY better: a file-object wrapper that sanitizes the output on-the-fly so that
        # pandas can then directly parse it. But I couldn't get that to work AT ALL...

        logger.info("📤  Reading hledger's output...")
        hledger_output, hledger_stderr = hledger.communicate()

        logger.debug(f"{hledger_stderr = }")
        if hledger_stderr:
            logger.warning(
                f"Command >>> {hledger_cmdline} <<< returned STDERR:\n{hledger_stderr}"
            )

        if not hledger_output:
            logger.info(
                f"Command >>> {hledger_cmdline} <<< returned no output."
            )
            sys.exit(0)

        if logger.getEffectiveLevel() < logging.DEBUG:
            console.print(
                Panel(
                    Syntax(
                        hledger_output,
                        "python",
                        line_numbers=True,
                    ),
                    title=f"Output of {hledger_cmdline}",
                )
            )

        logger.debug("Parsing output...")
        try:
            read_csv_args, read_csv_kwargs = [
                io.StringIO(hledger_output)
            ], dict(
                on_bad_lines="skip",
            )
            logger.debug(
                f"Running pd.read_csv(*{read_csv_args}, **{read_csv_kwargs})"
            )
            data = pd.read_csv(*read_csv_args, **read_csv_kwargs)

        except Exception as e:
            logger.exception(f"Error: {e}")
            logger.info(hledger_output)
            sys.exit(1)

        logger.debug("Converting times...")
        for col in ["period", "start_date", "end_date"]:
            if col in data:
                data[col] = pd.to_datetime(data[col], errors="coerce")

        logger.debug("Converting amounts...")
        for col in ["value"]:
            if col in data:
                data[col] = pd.to_numeric(data[col], errors="coerce")

        return data

    data = hledger_to_dataframe(hledger_cmdline_parts)
    commodities = list(data.commodity.unique())
    if not args.account_format:
        args.account_format = (
            "{account} ({commodity})" if len(commodities) > 1 else "{account}"
        )

    # Try to auto-format commodities right
    # TODO: Can we prevent this loop by using `hledger stats` for example to
    # know the commodities in advance? Although hledger stats also parses
    # everything so might not be much of a benefit...
    if missing_values := data["value"].isna().sum():
        logger.warning(
            f"There are {missing_values} NaNs in the converted amounts."
        )
        commodity_format_opts = list(
            itertools.chain.from_iterable(
                ("-c", f'1000000.0000 "{curr}"') for curr in commodities
            )
        )
        logger.info(f"Retrying with {shlex.join(commodity_format_opts)}")
        data = hledger_to_dataframe(
            hledger_cmdline_parts + commodity_format_opts
        )
        if missing_values := data["value"].isna().sum():
            logger.warning(
                f"Didn't help, trying to plot anyway but it'll look weird."
            )
        else:
            logger.info(f"That worked, no NaNs in the amounts anymore! 🎉 ")
            logger.info(
                f"Consider adding {shlex.join(commodity_format_opts)} "
                f"to your query to speed up hledger-plot."
            )

    time_columns = [col for col in data if hasattr(data[col], "dt")]
    logger.debug(f"Using minimum of {time_columns = } as time")
    data = data.set_index(data[time_columns].min(axis="columns"))
    data = data.drop(columns=time_columns)
    logger.debug(f"data = \n{data}")

    data["account"] = data["account"].astype(str)

    groupby = ["account", "commodity"]
    logger.info(f"Grouping accounts and commodities by {groupby}")
    account_commodities = {}
    data_to_concat = []
    for n, g in data.groupby(groupby):
        data_to_concat.append(
            g["value"].rename(
                newname := args.account_format.format(
                    **(m := dict(zip(groupby, n)))
                )
            )
        )
        account_commodities[newname] = m.get("commodity", "")
    data = pd.concat(
        data_to_concat,
        axis="columns",
    )
    logger.debug(f"{account_commodities = }")
    logger.debug(f"data = \n{data}")

    if args.terminal:
        try:
            matplotlib.use("module://drawilleplot")
        except Exception as e:
            logger.exception(
                f"Couldn't use drawilleplot as matplotlib backend. "
                f"Error: {e}"
            )
            logger.critical(
                f"""
Couldn't use drawilleplot as matplotlib backend. Error: {e}

Either try to fix that or remove the --terminal option.

You can try:

# checking if importing drawilleplot works
python -c 'import drawilleplot'

# re-running with MPLBACKEND variable (with and/or without --terminal)
MPLBACKEND='module://drawilleplot' hledger plot .....

# on Windows one apparently needs to install windows-curses:
pip install windows-curses
""".strip()
            )
            sys.exit(1)

    # some sane defaults for rcParams
    plt.rcParams["legend.handlelength"] = 5
    if len(data.columns) > 10:
        plt.rcParams["legend.fontsize"] = "x-small"
    elif len(data.columns) > 15:
        plt.rcParams["legend.fontsize"] = "xx-small"
    plt.rcParams["axes.grid"] = True
    plt.rcParams["axes.axisbelow"] = True
    # expand prop cycle
    prop_cycle = plt.rcParams["axes.prop_cycle"]
    if "linestyle" not in prop_cycle:
        prop_cycle = (
            cycler(linestyle=["solid", "dashed", "dotted"]) * prop_cycle
        )
    if "linewidth" not in prop_cycle:
        lw = plt.rcParams.get("lines.linewidth", 2)
        prop_cycle = (
            cycler(linewidth=[lw, lw + 1, lw + 2, lw + 3]) * prop_cycle
        )
    plt.rcParams["axes.prop_cycle"] = prop_cycle
    # logger.debug(f"{list(plt.rcParams['axes.prop_cycle']) = }")

    # merge all --rcParams options
    args.rcParams = functools.reduce(
        lambda a, b: {**a, **b}, filter(bool, args.rcParams), dict()
    )
    # overwrite with user's rcParams
    plt.rcParams.update(args.rcParams)

    # 🔢 Data Modification
    def invert_handler(patterns, data=data):
        for pattern in patterns:
            for col in data:
                if m := pattern.search(col):
                    logger.info(f"↔️  Inverting {col!r} amount")
                    data[col] = data[col] * -1
        return data

    # rename nan to actual "nan"
    data = data.rename(columns={x: str(x) for x in data})

    def rename_handler(mapping, data=data):
        logger.debug(f"{mapping = }")
        renames = dict(mapping)
        logger.info(f"Renaming columns: {renames}")
        return data.rename(columns=renames)

    def sum_handler(mapping, data=data):
        logger.debug(f"Applying --sum to {mapping = }")
        for pattern, newname in mapping:
            if columns := list(filter(pattern.search, data)):
                data[newname] = np.nansum(
                    [data[col] for col in columns], axis=0
                )
                logger.info(
                    f"Created new column {newname!r} summing {columns}"
                )
            else:
                logger.info(
                    f"🤷  No columns matching pattern {pattern.pattern!r}"
                )
        return data

    def mean_handler(mapping, data=data):
        logger.debug(f"{mapping = }")
        for pattern, newname in mapping:
            if columns := list(filter(pattern.search, data)):
                data[newname] = np.nanmean(
                    [data[col] for col in columns], axis=0
                )
                logger.info(
                    f"Created new column {newname!r} averaging {columns}"
                )
            else:
                logger.info(
                    f"🤷  No columns matching pattern {pattern.pattern!r}"
                )
        return data

    def multiply_handler(mapping, data=data):
        logger.debug(f"{mapping = }")
        for oldname, factor, newname in mapping:
            if oldname not in data:
                logger.error(
                    f"No such column {oldname!r} to multiply with {factor}"
                )
                continue
            data[newname] = data[oldname] * factor
        return data

    def resample_handler(intervals, data=data):
        logger.debug(f"{intervals = }")
        for interval in intervals:
            data = data.resample(interval).sum()
        return data

    def trend_handler(trenddefs, data=data):
        for trenddef in trenddefs:
            logger.debug(f"{trenddef = }")
            pattern, timerange, interval, reference = trenddef
            if interval is None:
                interval = next(
                    (
                        i
                        for x, i in dict(
                            daily=1,
                            weekly=7,
                            monthly=30,
                            quarterly=30 * 3,
                            yearly=360,
                        ).items()
                        if getattr(hledger_parsed_args, x, None)
                    ),
                    1,
                )
            if cols_to_fit := list(filter(pattern.search, data)):
                for col in cols_to_fit:
                    series = data.loc[timerange, col]
                    logger.debug(f"series = \n{series}")
                    days_since_reference = (
                        series.index.map(pd.Timestamp.timestamp)
                        - (reference.timestamp() if reference else 0)
                    ) / (24 * 60 * 60)
                    fit = scipy.stats.linregress(days_since_reference, series)

                    def oma(x):
                        # orders of magnitude in amounts
                        return (
                            int(np.ceil(np.log10(abs(x)))) if abs(x) > 0 else 0
                        )

                    def autofmt(x, showsign=False):
                        digits = np.clip(2 - oma(x), 0, None)
                        fmt = f"{{:{'+' if showsign else ''}.{digits}f}} {account_commodities.get(col,'')}"
                        return fmt.format(x)

                    logger.debug(f"{fit = }")
                    trend_colname_base = f"{col} trend"
                    trend_colname_slope = f"({autofmt(fit.slope * interval,showsign=True)}/{str(interval) if interval != 1 else ''}day{'s' if interval!=1 else ''})"
                    trend_colname_mean = f"⌀ = {autofmt(series.mean())}"
                    predicted = (
                        days_since_reference * fit.slope + fit.intercept
                    )
                    trend_colname = f"{trend_colname_base} {trend_colname_slope} {trend_colname_mean}"
                    if reference:
                        trend_colname_reference = f"{autofmt(fit.intercept)} @ {reference.strftime('%Y-%m-%d')}"
                        t = series.index
                        if not (t.min() <= reference <= t.max()):
                            i = 0 if reference < t.min() else (t.size - 1)
                            extrapolation = pd.Series(
                                [fit.intercept, predicted[i]],
                                name=f"{trend_colname_base} extrapolation {trend_colname_reference}",
                                index=[reference, t[i]],
                            ).sort_index()
                            logger.debug(f"extrapolation = \n{extrapolation}")
                            # add extrapolation to data
                            data = pd.concat(
                                [data, extrapolation.to_frame()],
                                axis="columns",
                            ).sort_index()
                            logger.debug(
                                f"after joining extrapolation: data = \n{data}"
                            )
                        else:
                            trend_colname = (
                                f"{trend_colname} {trend_colname_reference}"
                            )
                    data = pd.concat(
                        [
                            data,
                            pd.Series(
                                predicted,
                                name=trend_colname,
                                index=series.index,
                            ).to_frame(),
                        ],
                        axis="columns",
                    ).sort_index()
            else:
                logger.warning(
                    f"--trend pattern {pattern.pattern!r} didn't match any columns."
                )
        return data

    def drop_handler(mapping, data=data):
        for pattern in mapping:
            if columns := list(filter(pattern.search, data)):
                data = data.drop(columns=columns)
                logger.info(f"Dropped columns {columns!r}")
            else:
                logger.info(
                    f"🤷  No columns matching pattern {pattern.pattern!r}"
                )
        return data

    def only_handler(patterns, data=data):
        if columns := list(
            col for col in data if any(p.search(col) for p in patterns)
        ):
            data = data[columns]
            logger.info(f"Kept only columns {columns!r}")
        else:
            logger.info(f"🤷  No columns matching {patterns = }")
        return data

    modhandlers = dict(
        sum=sum_handler,
        invert=invert_handler,
        rename=rename_handler,
        mean=mean_handler,
        multiply=multiply_handler,
        drop=drop_handler,
        only=only_handler,
        resample=resample_handler,
        trend=trend_handler,
    )

    for step, (modname, index) in enumerate(args.mod_order, start=1):
        logger.debug(f"--mod-order step Nr. {step}: {modname = !r} {index = }")
        if (handler := modhandlers.get(modname)) and (
            ((allmodsteps := getattr(args, modname, None)) is not None)
        ):
            logger.debug(
                f"All {len(allmodsteps)} steps for {modname!r}: {allmodsteps = }"
            )
            if (
                1
                <= (index if isinstance(index, int) else -1)
                <= len(allmodsteps)
            ):
                modsteps = allmodsteps[(index - 1) : index]
            else:
                modsteps = allmodsteps
            if modsteps:
                logger.debug(f"Running {modname!r} steps {modsteps}")
                data = handler(modsteps, data=data)
                logger.debug(
                    f"data after {modname!r} with steps {modsteps}:\n{data}"
                )
            elif index is not None:
                logger.warning(f"No {modname!r} steps? ({index = })")
        else:
            logger.warning(
                f"No handler for --mod-order step {modname = !r} {index = } ({allmodsteps = })"
            )

    logger.info("📈  Plotting...")
    with plt.xkcd() if args.xkcd else nothing():
        fig, ax = plt.subplots(num=args.title)
        if args.barplot:
            logger.warning(
                f"Barplots are kind of limited right now and don't scale well."
            )
            if args.stacked:
                data.drop(
                    columns=["Total:", "total:"], inplace=True, errors="ignore"
                )
            data["Point in Time"] = data.index.strftime("%Y-%m-%d")
            data.plot.bar(ax=ax, x="Point in Time", stacked=args.stacked)
        else:

            def only_prop_cycle(d):
                return {
                    k: v
                    for k, v in d.items()
                    if k in plt.rcParams["axes.prop_cycle"].keys
                }

            used_styles = list()
            for column in data:
                series = data[column].dropna()
                plot_kwargs = dict(
                    drawstyle=args.drawstyle, label=column.replace(r"$", r"\$")
                )
                if args.style:
                    # apply styles
                    for pattern, kwargs in args.style:
                        if pattern.search(column):
                            plot_kwargs.update(kwargs)
                    logger.debug(f"after applying --styles {plot_kwargs = }")

                    if pc_kw := next(
                        (
                            pc
                            for pc in list(plt.rcParams["axes.prop_cycle"])
                            if not any(
                                s == only_prop_cycle({**pc, **plot_kwargs})
                                for s in used_styles
                            )
                        ),
                        None,
                    ):
                        logger.debug(
                            f"Found previously unused style: {pc_kw = }"
                        )
                        plot_kwargs = {**pc_kw, **plot_kwargs}
                        logger.debug(
                            f"after filling with prop_cycle: {plot_kwargs = }"
                        )
                ax.plot(series.index, series, **plot_kwargs)
                used_styles.append(only_prop_cycle(plot_kwargs))
                logger.debug(f"{used_styles = }")

            if not args.no_today:
                ax.axvline(
                    pd.to_datetime(datetime.datetime.now()),
                    alpha=0.2,
                    color="black",
                    linewidth=10,
                    linestyle="solid",
                    label="today",
                    zorder=-10,
                )

        if args.title:
            fig.suptitle(args.title)
        ax.set_title(args.axtitle or " ".join(hledger_args))
        ax.set_ylabel(" ".join(f"[{c}]" for c in commodities))
        ax.legend(ncols=math.ceil(len(ax.get_lines()) / 40))

        fig.tight_layout()
        fig.set_tight_layout(True)
        fig.autofmt_xdate()

        for output_file in flatten(args.output):
            logger.info(
                f"Saving plots with --terminal active "
                f"might result in {output_file!r} looking weird."
            )
            logger.info("📥  Saving plot to '{}'".format(output_file))
            if output_file.endswith(".pickle"):
                with open(output_file, "wb") as fh:
                    pickle.dump(fig, fh)
            else:
                fig.savefig(output_file)

        if not args.no_show:
            logger.info("👀  Showing plot...")
            plt.show()


if __name__ == "__main__":
    cli()
