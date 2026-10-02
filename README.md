# Pomodoro Focus CLI

Run focused work and break cycles from the terminal, record completed focus blocks in SQLite, and print a daily total by project.

## Quick start

```bash
python -m venv .venv
python -m pip install -e .
pomodoro start --project "Python practice" --cycles 4
pomodoro report
```

Defaults are 25 minutes of focus and 5 minutes of break, with a longer break after every fourth completed cycle. Use `--focus-minutes` and `--break-minutes` to adjust the timer. The database path can be set with `POMODORO_DB_PATH`.

## Notes

The timer uses the monotonic clock for elapsed time. A notification is best-effort; the session still completes if a desktop notification backend is unavailable. Only completed focus sessions are stored.

## Learning notes

Practice command-line subcommands, SQLite inserts and aggregates, a progress display, and separating scheduling rules from waiting and notification code.

## Development

```bash
python -m pip install -e ".[dev]"
pytest
```

## License

MIT. See [LICENSE](LICENSE).
