#!/usr/bin/env python3
"""
Normalize fractional rgb() colours emitted by modern dart-sass into plain hex.

Dart-sass >= 1.7x emits colour maths as `rgb(49.3, 164.05, 153.85)` where older
versions emitted `#31a49a`. Both are valid CSS, but the sister sites (sreday,
llmday, devopsnotdead) ship hex, so we normalize to keep the theme files
consistent and a little smaller.

Only 3-argument numeric rgb() is touched. rgba(), rgb(var(--x)) and anything
non-numeric are left exactly as they are.

Usage:
    python _build/normalize_css_colors.py path/to/theme.css [more.css ...]
"""

import re
import sys

# rgb( n , n , n ) where each n is a plain (possibly fractional) number
RGB_NUMERIC = re.compile(
    r"rgb\(\s*(\d+(?:\.\d+)?)\s*,\s*(\d+(?:\.\d+)?)\s*,\s*(\d+(?:\.\d+)?)\s*\)"
)


def _to_hex(match: re.Match) -> str:
    channels = []
    for raw in match.groups():
        value = int(round(float(raw)))
        channels.append(max(0, min(255, value)))
    return "#{:02x}{:02x}{:02x}".format(*channels)


def normalize(css: str) -> tuple[str, int]:
    return RGB_NUMERIC.subn(_to_hex, css)


def main(paths: list[str]) -> int:
    if not paths:
        print(__doc__.strip())
        return 1

    for path in paths:
        with open(path, "r", encoding="utf-8") as f:
            original = f.read()

        converted, count = normalize(original)

        if count:
            with open(path, "w", encoding="utf-8") as f:
                f.write(converted)
        saved = len(original) - len(converted)
        print(f"{path}: {count} rgb() -> hex ({saved} bytes saved)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
