import argparse
import os
from datetime import date
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

from .storage import FocusStore
from .timer import run_cycles


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Focus in timed blocks and keep a local log.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    start = subparsers.add_parser("start", help="run focus and break cycles")
    start.add_argument("--project", default="General study")
    start.add_argument("--cycles", type=int, default=4)
    start.add_argument("--focus-minutes", type=int, default=25)
    start.add_argument("--break-minutes", type=int, default=5)
    report = subparsers.add_parser("report", help="show today's logged focus time")
    report.add_argument("--date", type=date.fromisoformat, default=date.today())
    parser.add_argument("--db", type=Path, default=Path(os.getenv("POMODORO_DB_PATH", "~/.pomodoro/focus.sqlite3")))
    args = parser.parse_args(argv)
    store = FocusStore(args.db)
    if args.command == "start":
        if min(args.cycles, args.focus_minutes, args.break_minutes) <= 0:
            parser.error("cycle and duration values must be positive")
        run_cycles(store, args.project, args.cycles, args.focus_minutes, args.break_minutes, 15, 4)
    else:
        table = Table(title=f"Focus minutes · {args.date.isoformat()}")
        table.add_column("Project")
        table.add_column("Minutes", justify="right")
        for project, minutes in store.daily_totals(args.date):
            table.add_row(project, str(minutes))
        Console().print(table)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
