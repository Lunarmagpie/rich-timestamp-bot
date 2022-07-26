from __future__ import annotations

from typing import Sequence

__all__: Sequence[str] = ("TIME_FORMATS",)


TIME_FORMATS: list[tuple[str, str]] = [
    ("Short Time", "t"),
    ("Long Time", "T"),
    ("Short Date", "d"),
    ("Long Date", "D"),
    ("Short Date/Time", "f"),
    ("Long Date/Time", "F"),
    ("Relative Time", "R"),
]
