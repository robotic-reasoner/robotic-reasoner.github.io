#!/usr/bin/env python3
"""Find successful rollout videos from tmp/ and write draft.md.

Selection rule:
- Filenames encode scene_trial as <scene>_<trial> before _success.mp4
  (e.g. custom_gris_0_2_success.mp4 = scene 0, trial 2).
- Pick the first NUM_EXAMPLES successes from *different scenes*.
- Walk jobs in order (job0, job1, job2, ...); within each job, trajectories
  sorted by (scene, trial). Skip a success if its scene was already picked.
- If job0 lacks enough distinct scenes, continue into job1, job2, etc.

Run before prepare_task_videos.py:
  python scripts/find_task_examples.py
  python scripts/prepare_task_videos.py
"""

from __future__ import annotations

import re
from pathlib import Path

# --- CONFIG (edit these) ---
REPO_ROOT = Path(__file__).resolve().parents[1]
VIS_ROOT = REPO_ROOT / "tmp" / "vis_vlm_qwen35_v3_1_rendered_v2"
DRAFT_PATH = REPO_ROOT / "draft.md"
NUM_EXAMPLES = 2

# vis_<prefix>-... folder prefix -> draft.md section title (must match TASK_META)
VIS_PREFIX_TO_TITLE: dict[str, str] = {
    "group_color": "Group blocks (group)",
    "line_color": "Make a line (line)",
    "T": "Make a T-shape (T)",
    "V": "Make a V-shape (V)",
    "L": "Make an L-shape (L)",
    "rect": "Make a rectangle (rect)",
    "gris": "Group & isolate (gris)",
    "mid": "Make a midpoint (mid)",
    "clear_quarter": "Clear quarter (clear qtr)",
    "iip": "Isolate in place (iip)",
    "iV": "Make an inverted V-shape (iV)",
    "iL": "Make an inverted L-shape (iL)",
    "dline": "Make a diagonal line (diag line)",
    "clear_half": "Clear half (clear half)",
}

TASK_ORDER = list(VIS_PREFIX_TO_TITLE.keys())


def job_sort_key(name: str) -> int:
    match = re.match(r"job(\d+)_", name)
    if not match:
        raise ValueError(f"Unexpected job folder name: {name}")
    return int(match.group(1))


def parse_scene_trial(filename: str) -> tuple[int, int]:
    match = re.search(r"_(\d+)_(\d+)_success\.mp4$", filename)
    if not match:
        raise ValueError(f"Cannot parse scene/trial from filename: {filename}")
    return int(match.group(1)), int(match.group(2))


def vis_prefix(task_dir_name: str) -> str:
    name = task_dir_name[4:] if task_dir_name.startswith("vis_") else task_dir_name
    return re.split(r"-qwen", name)[0]


def find_task_dir(prefix: str) -> Path:
    matches = [
        p for p in VIS_ROOT.iterdir()
        if p.is_dir() and vis_prefix(p.name) == prefix
    ]
    if not matches:
        raise FileNotFoundError(f"No vis folder for prefix {prefix!r} under {VIS_ROOT}")
    if len(matches) > 1:
        raise RuntimeError(f"Multiple vis folders for prefix {prefix!r}: {matches}")
    return matches[0]


def find_examples(task_dir: Path, n: int) -> list[tuple[str, int, int, Path]]:
    picks: list[tuple[str, int, int, Path]] = []
    seen_scenes: set[int] = set()

    jobs = sorted(
        [d for d in task_dir.iterdir() if d.is_dir() and d.name.startswith("job")],
        key=lambda p: job_sort_key(p.name),
    )
    for job_dir in jobs:
        videos_dir = job_dir / "videos"
        if not videos_dir.is_dir():
            continue

        successes = sorted(
            [f for f in videos_dir.iterdir() if f.name.endswith("_success.mp4")],
            key=lambda p: parse_scene_trial(p.name),
        )
        for video in successes:
            scene, trial = parse_scene_trial(video.name)
            if scene in seen_scenes:
                continue
            seen_scenes.add(scene)
            job_label = f"job{job_sort_key(job_dir.name)}"
            picks.append((job_label, scene, trial, video))
            if len(picks) >= n:
                return picks

    if len(picks) < n:
        raise RuntimeError(
            f"Task {task_dir.name}: found {len(picks)} distinct-scene successes, need {n}"
        )
    return picks


def to_repo_rel(path: Path) -> str:
    rel = path.relative_to(REPO_ROOT)
    return rel.as_posix()


def write_draft(rows: list[tuple[str, list[tuple[str, int, int, Path]]]]) -> None:
    lines = ["# Example of successful evaluation rollouts (ours)", ""]
    lines.append(
        f"Auto-selected: first {NUM_EXAMPLES} successes from distinct scenes "
        f"(scene_trial in filename). Jobs searched in order job0, job1, ..."
    )
    lines.append("")

    for title, picks in rows:
        lines.append(f"## {title}")
        lines.append("")
        for i, (job_label, scene, trial, path) in enumerate(picks, 1):
            lines.append(
                f"example {i} ({job_label}, scene {scene}, trial {trial}): "
                f"{to_repo_rel(path)}"
            )
        lines.append("")

    DRAFT_PATH.write_text("\n".join(lines))
    print(f"Wrote {DRAFT_PATH.relative_to(REPO_ROOT)}")


def main() -> None:
    if not VIS_ROOT.is_dir():
        raise FileNotFoundError(f"Rendered videos not found: {VIS_ROOT}")

    rows: list[tuple[str, list[tuple[str, int, int, Path]]]] = []
    for prefix in TASK_ORDER:
        title = VIS_PREFIX_TO_TITLE[prefix]
        task_dir = find_task_dir(prefix)
        picks = find_examples(task_dir, NUM_EXAMPLES)
        rows.append((title, picks))
        summary = ", ".join(
            f"{job} scene{s}_trial{t}" for job, s, t, _ in picks
        )
        print(f"OK {title}: {summary}")

    write_draft(rows)


if __name__ == "__main__":
    main()
