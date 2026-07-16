#!/usr/bin/env python3
"""Re-encode MP4 videos under static/ to browser-compatible H.264.

Use this if you already copied videos manually and only need the web codec fix.
For the full copy + HTML update workflow, use prepare_task_videos.py instead.

Requires ffmpeg and ffprobe on PATH.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

# --- CONFIG (edit these) ---
REPO_ROOT = Path(__file__).resolve().parents[1]
VIDEO_ROOT = REPO_ROOT / "static" / "task_examples_ours"

FFMPEG_CRF = 23
FFMPEG_PRESET = "medium"


def require_tool(name: str) -> None:
    if shutil.which(name) is None:
        raise RuntimeError(f"Required tool not found on PATH: {name}")


def get_codec(path: Path) -> str:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=codec_name",
            "-of",
            "csv=p=0",
            str(path),
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
        print(f"skip (already h264): {path.relative_to(REPO_ROOT)}")
        return

    tmp = path.with_suffix(".web.tmp.mp4")
    print(f"re-encode ({get_codec(path)} -> h264): {path.relative_to(REPO_ROOT)}")

    result = subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(path),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-preset",
            FFMPEG_PRESET,
            "-crf",
            str(FFMPEG_CRF),
            "-movflags",
            "+faststart",
            "-an",
            str(tmp),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        tmp.unlink(missing_ok=True)
        raise RuntimeError(f"ffmpeg failed for {path}:\n{result.stderr[-2000:]}")

    tmp.replace(path)


def main() -> None:
    require_tool("ffmpeg")
    require_tool("ffprobe")

    if not VIDEO_ROOT.is_dir():
        raise FileNotFoundError(f"Video directory not found: {VIDEO_ROOT}")

    videos = sorted(VIDEO_ROOT.rglob("*.mp4"))
    if not videos:
        raise ValueError(f"No .mp4 files found under {VIDEO_ROOT}")

    for video in videos:
        reencode_video(video)

    non_h264 = [
        p for p in videos if get_codec(p) != "h264"
    ]
    if non_h264:
        raise RuntimeError(f"Some videos are still not h264: {non_h264}")

    print(f"Done. Re-encoded {len(videos)} videos under {VIDEO_ROOT.relative_to(REPO_ROOT)}/")


if __name__ == "__main__":
    main()
