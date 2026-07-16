#!/usr/bin/env python3
"""Copy rollout videos from draft.md and re-encode them for GitHub Pages.

Workflow:
1. Run: python scripts/find_task_examples.py   (optional; writes draft.md)
2. Or edit draft.md manually with source paths.
3. Run: python scripts/prepare_task_videos.py
4. Commit static/task_examples_ours/ (and index.html if UPDATE_HTML is True).
5. Push to main; GitHub Pages deploys automatically.

Requires ffmpeg and ffprobe on PATH.
"""

from __future__ import annotations

import html
import re
import shutil
import subprocess
from pathlib import Path

# --- CONFIG (edit these) ---
REPO_ROOT = Path(__file__).resolve().parents[1]
DRAFT_PATH = REPO_ROOT / "draft.md"
DEST_ROOT = REPO_ROOT / "static" / "task_examples_ours"
INDEX_PATH = REPO_ROOT / "index.html"

UPDATE_HTML = True
REENCODE_FOR_WEB = True
CLEAN_DEST_BEFORE_COPY = True
NUM_EXAMPLES = 2

FFMPEG_CRF = 23
FFMPEG_PRESET = "medium"

TASK_META: dict[str, tuple[str, bool]] = {
    "Group blocks (group)": ("group_color", False),
    "Make a line (line)": ("line_color", False),
    "Make a T-shape (T)": ("T", True),
    "Make a V-shape (V)": ("V", True),
    "Make an L-shape (L)": ("L", True),
    "Make a rectangle (rect)": ("rect", False),
    "Group & isolate (gris)": ("gris", False),
    "Make a midpoint (mid)": ("mid", False),
    "Clear quarter (clear qtr)": ("clear_quarter", False),
    "Isolate in place (iip)": ("iip", False),
    "Make an inverted V-shape (iV)": ("iV", True),
    "Make an inverted L-shape (iL)": ("iL", True),
    "Make a diagonal line (diag line)": ("dline", False),
    "Clear half (clear half)": ("clear_half", False),
}


def require_tool(name: str) -> None:
    if shutil.which(name) is None:
        raise RuntimeError(f"Required tool not found on PATH: {name}")


def parse_draft(path: Path) -> list[tuple[str, list[str]]]:
    if not path.is_file():
        raise FileNotFoundError(f"Draft file not found: {path}")

    tasks: list[tuple[str, list[str]]] = []
    current: str | None = None
    examples: list[str] = []

    for line in path.read_text().splitlines():
        if line.startswith("## "):
            if current is not None:
                if len(examples) != NUM_EXAMPLES:
                    raise ValueError(
                        f"Task {current!r} must have exactly {NUM_EXAMPLES} examples; "
                        f"got {len(examples)}"
                    )
                tasks.append((current, examples))
            current = line[3:].strip()
            examples = []
        elif line.startswith("example "):
            # "example 1: path" or "example 1 (job0, scene 0, trial 2): path"
            examples.append(line.split(": ", 1)[1].strip())

    if current is not None:
        if len(examples) != NUM_EXAMPLES:
            raise ValueError(
                f"Task {current!r} must have exactly {NUM_EXAMPLES} examples; "
                f"got {len(examples)}"
            )
        tasks.append((current, examples))

    if not tasks:
        raise ValueError(f"No tasks found in {path}")

    return tasks


def parse_scene_trial(filename: str) -> tuple[str, str]:
    match = re.search(r"_(\d+)_(\d+)_success\.mp4$", filename)
    if not match:
        raise ValueError(f"Cannot parse scene/trial from filename: {filename}")
    return match.group(1), match.group(2)


def parse_job_dir(path: str) -> str:
    match = re.search(r"/(job\d+)_", path)
    if not match:
        raise ValueError(f"Cannot parse job folder from path: {path}")
    return match.group(1)


def dest_filename(slug: str, use_shape: bool, scene: str, trial: str) -> str:
    if use_shape:
        return f"custom_{slug}_shape_{scene}_{trial}_success.mp4"
    return f"custom_{slug}_{scene}_{trial}_success.mp4"


def dest_rel_path(slug: str, job_dir: str, filename: str) -> str:
    return f"./static/task_examples_ours/{slug}/{job_dir}/{filename}"


def get_codec(path: Path) -> str:
    result = subprocess.run(
        [
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=codec_name", "-of", "csv=p=0", str(path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    codec = result.stdout.strip()
    if not codec:
        raise RuntimeError(f"Could not detect video codec: {path}")
    return codec


def reencode_video(path: Path) -> None:
    if get_codec(path) == "h264":
        print(f"  skip re-encode (already h264): {path.relative_to(REPO_ROOT)}")
        return

    tmp = path.with_suffix(".web.tmp.mp4")
    print(f"  re-encode ({get_codec(path)} -> h264): {path.relative_to(REPO_ROOT)}")

    result = subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(path),
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-preset", FFMPEG_PRESET, "-crf", str(FFMPEG_CRF),
            "-movflags", "+faststart", "-an", str(tmp),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        tmp.unlink(missing_ok=True)
        raise RuntimeError(f"ffmpeg failed for {path}:\n{result.stderr[-2000:]}")

    tmp.replace(path)
    if get_codec(path) != "h264":
        raise RuntimeError(f"Re-encode did not produce h264: {path}")


def copy_tasks(tasks: list[tuple[str, list[str]]]) -> list[tuple[str, list[str]]]:
    if CLEAN_DEST_BEFORE_COPY and DEST_ROOT.exists():
        shutil.rmtree(DEST_ROOT)

    html_rows: list[tuple[str, list[str]]] = []

    for title, source_paths in tasks:
        if title not in TASK_META:
            raise KeyError(
                f"Unknown task title {title!r}. Add it to TASK_META in prepare_task_videos.py"
            )

        slug, use_shape = TASK_META[title]
        dest_paths: list[str] = []

        for rel in source_paths:
            src = REPO_ROOT / rel
            if not src.is_file():
                raise FileNotFoundError(f"Source video not found: {src}")

            job_dir = parse_job_dir(rel)
            scene, trial = parse_scene_trial(src.name)
            filename = dest_filename(slug, use_shape, scene, trial)
            dest_dir = DEST_ROOT / slug / job_dir
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest = dest_dir / filename

            shutil.copy2(src, dest)
            if REENCODE_FOR_WEB:
                reencode_video(dest)

            dest_paths.append(dest_rel_path(slug, job_dir, filename))

        html_rows.append((title, dest_paths))
        print(f"OK {title}: " + " , ".join(dest_paths))

    return html_rows


def html_title_pattern(title: str) -> str:
    """Match title in index.html whether & is written as & or &amp;."""
    escaped = re.escape(title)
    return escaped.replace(r"\&", r"(?:&amp;|&)")


def render_rollout_section(title: str, vids: list[str]) -> str:
    columns = []
    for i, vid in enumerate(vids, 1):
        columns.append(
            f"""        <div class="column">
          <div class="item">
            <video controls muted playsinline preload="metadata">
              <source src="{vid}" type="video/mp4">
            </video>
            <p class="caption has-text-centered">Example {i}</p>
          </div>
        </div>"""
        )
    return f"""  <section class="section rollout-section">
    <div class="container">
      <h2 class="title is-4 has-text-centered">{html.escape(title)}</h2>
      <div class="columns is-vcentered rollout-row">
{chr(10).join(columns)}
      </div>
    </div>
  </section>"""


def update_index_html(html_rows: list[tuple[str, list[str]]]) -> None:
    if not INDEX_PATH.is_file():
        raise FileNotFoundError(f"index.html not found: {INDEX_PATH}")

    html = INDEX_PATH.read_text()
    for title, vids in html_rows:
        pattern = (
            rf'  <section class="section rollout-section">\s*'
            rf'<div class="container">\s*'
            rf'<h2 class="title is-4 has-text-centered">{html_title_pattern(title)}</h2>\s*'
            rf'<div class="columns is-vcentered rollout-row">.*?</div>\s*'
            rf'</div>\s*'
            rf'</section>'
        )
        replacement = render_rollout_section(title, vids)
        new_html, count = re.subn(pattern, replacement, html, count=1, flags=re.DOTALL)
        if count != 1:
            raise RuntimeError(
                f"Could not update index.html section for task {title!r} (matched {count} times)."
            )
        html = new_html

    INDEX_PATH.write_text(html)
    print(f"Updated video paths in {INDEX_PATH.relative_to(REPO_ROOT)}")


def main() -> None:
    require_tool("ffmpeg")
    require_tool("ffprobe")

    tasks = parse_draft(DRAFT_PATH)
    html_rows = copy_tasks(tasks)

    if UPDATE_HTML:
        update_index_html(html_rows)

    print(
        f"\nDone. Copied {sum(len(r[1]) for r in html_rows)} videos to "
        f"{DEST_ROOT.relative_to(REPO_ROOT)}/"
    )
    print("Next: git add static/task_examples_ours/ index.html && git commit && git push")


if __name__ == "__main__":
    main()
