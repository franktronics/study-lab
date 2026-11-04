"""Create a new studio folder with brief.md and scene.py templates.

    uv run python -m studylab_manim.new <slug>      # -> studio/YYYY-MM-DD-<slug>/
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys

from . import config as cfg

BRIEF = """\
# {id}

- **Goal**: <what the student should understand after watching>
- **Concept**: <the single concept explained>
- **Language**: <language of the on-screen text = language of the user's request>
- **Theme**: dark
- **Memo entry**: <tools/memo/<topic>/<file>.md>

## Sources
- assets/<file>, p. <pages>

## Storyboard
1. Scene `Intro` — title card
2. Scene `Main` — ...
3. Scene `Recap` — end card with key points
"""

SCENE = '''\
from manim import *

from studylab_manim import StudyScene


class Main(StudyScene):
    def construct(self):
        self.title_card("Title", "Subtitle")
        self.section("Section")
        self.caption("Explanation shown at the bottom of the screen.")
        self.wait()
'''


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a new studio folder.")
    parser.add_argument("slug", help="kebab-case English slug, e.g. gibbs-phenomenon")
    args = parser.parse_args()

    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", args.slug):
        sys.exit("Slug must be kebab-case: lowercase letters, digits and dashes.")
    studio_id = f"{dt.date.today().isoformat()}-{args.slug}"
    folder = cfg.STUDIO_DIR / studio_id
    if folder.exists():
        sys.exit(f"Already exists: {folder}")
    folder.mkdir(parents=True)
    (folder / "brief.md").write_text(BRIEF.format(id=studio_id), encoding="utf-8")
    (folder / "scene.py").write_text(SCENE, encoding="utf-8")
    print(f"CREATED {folder}")


if __name__ == "__main__":
    main()
