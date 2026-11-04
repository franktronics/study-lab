"""Check that everything needed to render is installed.

    uv run python -m studylab_manim.check

Prints one line per requirement (OK / MISSING) and exits with 1 if anything is missing.
"""

from __future__ import annotations

import shutil
import subprocess
import sys

from . import config as cfg


def main() -> None:
    cfg.ensure_tex_on_path()
    results: list[tuple[bool, str]] = []

    results.append((sys.version_info[:2] == (3, 12), f"python 3.12 (found {sys.version.split()[0]})"))

    try:
        import manim
        import manimpango  # noqa: F401  (text rendering)
        import cairo  # noqa: F401  (vector rendering)

        results.append((True, f"manim {manim.__version__}"))
    except ImportError as e:
        results.append((False, f"python packages ({e.name}) -> run `uv sync`"))

    for binary in ("latex", "dvisvgm"):
        results.append((shutil.which(binary) is not None, f"{binary} (LaTeX)"))

    kpsewhich = shutil.which("kpsewhich")
    if kpsewhich:
        for name in cfg.TEX_FILES:
            found = subprocess.run([kpsewhich, name], capture_output=True, text=True).stdout.strip()
            results.append((bool(found), f"LaTeX file {name}"))
    else:
        results.append((False, "kpsewhich (LaTeX)"))

    for ok, label in results:
        print(f"{'OK     ' if ok else 'MISSING'} {label}")
    missing = [label for ok, label in results if not ok]
    if missing:
        print(f"\n{len(missing)} missing. Required LaTeX packages: {' '.join(cfg.TEX_PACKAGES)}")
        sys.exit(1)
    print("\nAll good.")


if __name__ == "__main__":
    main()
