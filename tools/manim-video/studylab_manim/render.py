"""Render a studio video.

    uv run python -m studylab_manim.render <studio-id | path/to/file.py> [--quality preview|final]
                                           [--theme dark|light] [--frames N] [--scenes A B ...]

- Renders every scene of studio/<id>/scene.py in definition order (or --scenes).
- Concatenates them into one video:
    preview -> .cache/<id>/preview.mp4
    final   -> studio/<id>/<id>.mp4   (a plain .py file outside studio/: .cache/<name>/<name>.mp4)
- Extracts N evenly spaced frames + the last frame of each scene into
  .cache/<id>/frames/ for visual checks (default: 4 for preview, 0 for final).
"""

from __future__ import annotations

import argparse
import ast
import os
import shutil
import subprocess
import sys
from pathlib import Path

import av

from . import config as cfg
from .theme import THEME_ENV, THEMES


def scene_names(scene_file: Path) -> list[str]:
    """Scene classes in definition order, skipping classes only used as bases and private ones."""
    tree = ast.parse(scene_file.read_text(encoding="utf-8"))
    classes = [n for n in tree.body if isinstance(n, ast.ClassDef)]
    used_as_base = {b.id for c in classes for b in c.bases if isinstance(b, ast.Name)}
    names = []
    for c in classes:
        base_names = [b.id if isinstance(b, ast.Name) else getattr(b, "attr", "") for b in c.bases]
        is_scene = any(n.endswith("Scene") for n in base_names)
        if is_scene and c.name not in used_as_base and not c.name.startswith("_"):
            names.append(c.name)
    return names


def render_scenes(scene_file: Path, scenes: list[str], quality: str, theme: str, media: Path) -> list[Path]:
    flag, fps, subdir = cfg.QUALITIES[quality]
    cmd = [
        sys.executable, "-m", "manim", "render", flag,
        "--fps", str(fps),
        "--media_dir", str(media),
        "--progress_bar", "none",
        "--verbosity", "WARNING",
        str(scene_file), *scenes,
    ]  # fmt: skip
    env = {**os.environ, THEME_ENV: theme}
    result = subprocess.run(cmd, cwd=scene_file.parent, env=env)
    if result.returncode != 0:
        sys.exit(f"Render failed (exit {result.returncode}). See the Manim output above.")
    videos = media / "videos" / scene_file.stem / subdir
    outputs = [videos / f"{s}.mp4" for s in scenes]
    missing = [p for p in outputs if not p.exists()]
    if missing:
        sys.exit(f"Render produced no file for: {', '.join(p.stem for p in missing)}")
    return outputs


def concat(inputs: list[Path], output: Path) -> None:
    """Losslessly concatenate videos that share the same encoding settings."""
    output.parent.mkdir(parents=True, exist_ok=True)
    if len(inputs) == 1:
        shutil.copyfile(inputs[0], output)
        return
    with av.open(str(output), "w") as out:
        with av.open(str(inputs[0])) as first:
            stream = out.add_stream_from_template(first.streams.video[0])
        offset = 0
        for path in inputs:
            with av.open(str(path)) as inp:
                src = inp.streams.video[0]
                end = offset
                for packet in inp.demux(src):
                    if packet.dts is None:
                        continue
                    packet.pts += offset
                    packet.dts += offset
                    end = max(end, packet.pts + (packet.duration or 0))
                    packet.stream = stream
                    out.mux(packet)
                offset = end


def extract_frames(video: Path, out_dir: Path, count: int) -> list[Path]:
    """Save `count` evenly spaced frames plus the last frame of `video` as PNG."""
    saved: list[Path] = []
    with av.open(str(video)) as container:
        stream = container.streams.video[0]
        duration = float(stream.duration * stream.time_base) if stream.duration else container.duration / av.time_base
        targets = [duration * (i + 1) / (count + 1) for i in range(count)]
        last = None
        for frame in container.decode(stream):
            last = frame
            if targets and frame.time is not None and frame.time >= targets[0]:
                path = out_dir / f"{video.stem}_{len(saved) + 1:02d}_{frame.time:05.1f}s.png"
                frame.to_image().save(path)
                saved.append(path)
                targets.pop(0)
        if last is not None:
            path = out_dir / f"{video.stem}_last_{last.time or 0:05.1f}s.png"
            last.to_image().save(path)
            saved.append(path)
    return saved


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a studio video.")
    parser.add_argument("target", help="studio folder name (e.g. 2026-11-04-gibbs-phenomenon) or path to a .py file")
    parser.add_argument("--quality", choices=cfg.QUALITIES, default="preview")
    parser.add_argument("--theme", choices=THEMES, default="dark")
    parser.add_argument("--frames", type=int, default=None, help="frames per scene to extract")
    parser.add_argument("--scenes", nargs="+", help="render only these scenes, in this order")
    args = parser.parse_args()

    cfg.ensure_tex_on_path()
    if args.target.endswith(".py"):
        scene_file = Path(args.target).resolve()
        name = scene_file.stem
        final_output = cfg.CACHE_DIR / name / f"{name}.mp4"
    else:
        name = args.target
        scene_file = cfg.STUDIO_DIR / name / "scene.py"
        final_output = scene_file.parent / f"{name}.mp4"
    if not scene_file.exists():
        sys.exit(f"Not found: {scene_file}")
    scenes = args.scenes or scene_names(scene_file)
    if not scenes:
        sys.exit(f"No scene class found in {scene_file.name}.")

    cache = cfg.CACHE_DIR / name
    clips = render_scenes(scene_file, scenes, args.quality, args.theme, cache / "media")

    output = final_output if args.quality == "final" else cache / "preview.mp4"
    concat(clips, output)
    print(f"\nVIDEO {output}")

    frames = args.frames if args.frames is not None else (4 if args.quality == "preview" else 0)
    if frames or args.quality == "preview":
        frames_dir = cache / "frames"
        shutil.rmtree(frames_dir, ignore_errors=True)
        frames_dir.mkdir(parents=True)
        for clip in clips:
            for path in extract_frames(clip, frames_dir, frames):
                print(f"FRAME {path}")


if __name__ == "__main__":
    main()
