from __future__ import annotations

import sqlite3
from datetime import date
from pathlib import Path


class FocusStore:
    def __init__(self, path: Path):
        self.path = path.expanduser()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as connection:
            connection.execute("CREATE TABLE IF NOT EXISTS focus_sessions (id INTEGER PRIMARY KEY, project TEXT NOT NULL, started_at TEXT NOT NULL, minutes INTEGER NOT NULL CHECK(minutes > 0))")

    def add_session(self, project: str, started_at: str, minutes: int) -> None:
        if minutes <= 0:
            raise ValueError("minutes must be positive")
        with sqlite3.connect(self.path) as connection:
            connection.execute("INSERT INTO focus_sessions(project, started_at, minutes) VALUES (?, ?, ?)",
                               (project, started_at, minutes))

    def daily_totals(self, day: date) -> list[tuple[str, int]]:
        with sqlite3.connect(self.path) as connection:
            return connection.execute("SELECT project, SUM(minutes) FROM focus_sessions WHERE date(started_at) = ? GROUP BY project ORDER BY project",
                                      (day.isoformat(),)).fetchall()
