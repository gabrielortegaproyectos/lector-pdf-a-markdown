from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path

DAILY_PAGE_LIMIT = 900
USAGE_FILE = Path("/tmp/lector_pdf_to_md_daily_usage.json")


@dataclass
class UsageState:
    current_date: str
    used_pages: int


def _default_state() -> UsageState:
    return UsageState(current_date=date.today().isoformat(), used_pages=0)


def load_usage_state() -> UsageState:
    if not USAGE_FILE.exists():
        return _default_state()

    try:
        raw = json.loads(USAGE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return _default_state()

    state = UsageState(
        current_date=str(raw.get("current_date", date.today().isoformat())),
        used_pages=int(raw.get("used_pages", 0)),
    )
    if state.current_date != date.today().isoformat():
        return _default_state()
    return state


def save_usage_state(state: UsageState) -> None:
    USAGE_FILE.write_text(
        json.dumps(
            {
                "current_date": state.current_date,
                "used_pages": state.used_pages,
            }
        ),
        encoding="utf-8",
    )


def get_remaining_pages() -> int:
    state = load_usage_state()
    return max(0, DAILY_PAGE_LIMIT - state.used_pages)


def can_process_pages(requested_pages: int) -> bool:
    return requested_pages <= get_remaining_pages()


def register_processed_pages(processed_pages: int) -> UsageState:
    state = load_usage_state()
    state.used_pages = min(DAILY_PAGE_LIMIT, state.used_pages + processed_pages)
    save_usage_state(state)
    return state
