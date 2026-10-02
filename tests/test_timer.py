from pomodoro_cli.timer import break_minutes_after
from pomodoro_cli.storage import FocusStore
from datetime import date


def test_fourth_cycle_uses_long_break():
    assert break_minutes_after(3) == 5
    assert break_minutes_after(4) == 15


def test_completed_focus_blocks_are_grouped_by_project_and_date(tmp_path):
    store = FocusStore(tmp_path / "focus.sqlite3")
    store.add_session("Python", "2026-10-02T08:00:00+00:00", 25)
    store.add_session("Python", "2026-10-02T09:00:00+00:00", 25)
    assert store.daily_totals(date(2026, 10, 2)) == [("Python", 50)]
