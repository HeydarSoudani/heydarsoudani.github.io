#!/usr/bin/env python3
"""Assemble index.html from _template.html and the files in sections/.

Every <div data-include="path"></div> in the template is replaced by the
contents of that file, re-indented to sit where the placeholder sat.

    ./build.py           write index.html
    ./build.py --check   exit 1 if index.html is stale (nothing written)
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
TEMPLATE = ROOT / "_template.html"
OUTPUT = ROOT / "index.html"

BANNER = """<!--
  GENERATED FILE — DO NOT EDIT.
  Built from _template.html + sections/ by build.py. Edit those instead,
  then run ./build.py to regenerate this file.
-->
"""

PLACEHOLDER = re.compile(r'^([ \t]*)<div data-include="([^"]+)"></div>[ \t]*$', re.M)

# Notes meant for whoever edits the template, not for the built page.
SOURCE_ONLY = re.compile(r'^[ \t]*<!--[ \t]*build:source-only\b.*?-->[ \t]*\n', re.S | re.M)


def render():
    def replace(match):
        indent, rel = match.group(1), match.group(2)
        path = ROOT / rel
        if not path.is_file():
            sys.exit(f"build.py: {TEMPLATE.name} includes missing file: {rel}")
        lines = path.read_text().rstrip("\n").split("\n")
        # Blank lines stay blank so the output has no trailing whitespace.
        return "\n".join(indent + line if line.strip() else "" for line in lines)

    html, count = PLACEHOLDER.subn(replace, TEMPLATE.read_text())
    if count == 0:
        sys.exit("build.py: no data-include placeholders found in " + TEMPLATE.name)

    # Sits after the doctype so the file still opens with <!DOCTYPE html>.
    html = SOURCE_ONLY.sub("", html)
    html = html.replace("<!DOCTYPE html>\n", "<!DOCTYPE html>\n" + BANNER, 1)
    return html, count


def main():
    html, count = render()

    if "--check" in sys.argv:
        current = OUTPUT.read_text() if OUTPUT.exists() else None
        if current != html:
            sys.exit(f"build.py: {OUTPUT.name} is out of date — run ./build.py")
        print(f"{OUTPUT.name} is up to date ({count} sections)")
        return

    OUTPUT.write_text(html)
    print(f"Wrote {OUTPUT.name} ({count} sections, {len(html.splitlines())} lines)")


if __name__ == "__main__":
    main()
