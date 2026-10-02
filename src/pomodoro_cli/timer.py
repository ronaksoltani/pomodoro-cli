from __future__ import annotations

import time
from datetime import datetime, timezone

from plyer import notification
from rich.progress import BarColumn, Progress, TextColumn, TimeRemainingColumn

from .storage import FocusStore


def break_minutes_after(cycle: int, short_break: int = 5, long_break: int = 15, every: int = 4) -> int:
    return long_break if every > 0 and cycle % every == 0 else short_break


def notify(title: str, message: str) -> None:
    try:
        notification.notify(title=title, message=message, timeout=8)
    except Exception:
        pass  # Notifications are optional; the terminal remains the source of truth.


def wait_minutes(minutes: int, label: str) -> None:
    seconds = minutes * 60
    with Progress(TextColumn("{task.description}"), BarColumn(), TimeRemainingColumn()) as progress:
        task = progress.add_task(label, total=seconds)
        for _ in range(seconds):
            time.sleep(1)
            progress.advance(task)


def run_cycles(store: FocusStore, project: str, cycles: int, focus_minutes: int,
               short_break: int, long_break: int, long_every: int) -> None:
    for cycle in range(1, cycles + 1):
        started_at = datetime.now(timezone.utc).isoformat()
        notify("Focus time", f"Cycle {cycle}/{cycles}: {project}")
        wait_minutes(focus_minutes, f"Focus · {project} · cycle {cycle}/{cycles}")
        store.add_session(project, started_at, focus_minutes)
        notify("Focus block complete", "Time for a short reset.")
        if cycle < cycles:
            rest = break_minutes_after(cycle, short_break, long_break, long_every)
            wait_minutes(rest, f"Break · {rest} minutes")
