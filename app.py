import os
import sys
import shutil
import subprocess
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"

# Supported video extensions
SUPPORTED_EXTENSIONS = {".mp4", ".mov", ".mkv", ".avi", ".webm", ".m4v", ".flv"}


def compress_video(input_path, output_path=None, crf=22, codec="h264"):
    """
    Compress a video file with maximum device compatibility.

    codec="h264": Universally playable across all devices, browsers, and players (default).
    codec="h265": Smaller file size, but requires HEVC playback support on device.
    """
    input_path = Path(input_path).resolve()

    if not input_path.is_file():
        print(f"Error: Input video not found at '{input_path}'.")
        return None

    if not shutil.which("ffmpeg"):
        print("Error: FFmpeg is not installed or not found in system PATH.")
        return None

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if output_path is None:
        output_path = OUTPUT_DIR / f"{input_path.stem}_compressed.mp4"
    else:
        output_path = Path(output_path).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)

    original_size = input_path.stat().st_size

    print("=" * 60)
    print(f"Input file:      {input_path.name}")
    print(f"Original size:   {original_size / (1024**2):.2f} MB")
    print(f"Target output:   {output_path.name}")
    print(f"Encoding codec:  {codec.upper()} (Universal compatibility mode)")
    print("=" * 60)

    if codec.lower() in ("h265", "hevc", "x265"):
        # H.265 / HEVC mode
        v_codec = "libx265"
        extra_vflags = ["-tag:v", "hvc1"]
    else:
        # H.264 / AVC mode (100% universal across all browsers, Apple QuickTime, Windows, Android)
        v_codec = "libx264"
        extra_vflags = ["-profile:v", "high", "-level", "4.1"]

    command = [
        "ffmpeg",
        "-y",
        "-i", str(input_path),
        "-map", "0:v:0",
        "-map", "0:a?",
        "-c:v", v_codec,
        "-preset", "medium",
        "-crf", str(crf),
        "-pix_fmt", "yuv420p",
        *extra_vflags,
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        str(output_path)
    ]

    result = subprocess.run(command)

    if result.returncode != 0:
        print("\nCompression failed.")
        return None

    compressed_size = output_path.stat().st_size
    saved = original_size - compressed_size
    percentage = (saved / original_size) * 100 if original_size > 0 else 0

    print("\n" + "=" * 60)
    print("Compression completed successfully!")
    print(f"Original size:   {original_size / (1024**2):.2f} MB")
    print(f"Compressed size: {compressed_size / (1024**2):.2f} MB")
    print(f"Space saved:     {percentage:.2f}%")
    print(f"Output saved to: {output_path}")
    print("=" * 60 + "\n")
    return output_path


def find_input_videos():
    if not INPUT_DIR.exists() or not INPUT_DIR.is_dir():
        return []
    return [
        item for item in sorted(INPUT_DIR.iterdir())
        if item.is_file()
        and item.suffix.lower() in SUPPORTED_EXTENSIONS
        and not item.name.startswith(".")
    ]


def main():
    default_crf = int(os.environ.get("CRF", "22"))

    # 1. Explicit path passed via CLI argument: python app.py path/to/video.mp4
    if len(sys.argv) > 1:
        target = sys.argv[1].strip().strip('"\'')
        compress_video(target, crf=default_crf)
        return

    # 2. Check input directory automatically
    input_videos = find_input_videos()
    if input_videos:
        print(f"Found {len(input_videos)} video(s) in input/ folder:")
        for idx, video in enumerate(input_videos, start=1):
            print(f"  {idx}. {video.name} ({video.stat().st_size / (1024**2):.2f} MB)")
        print()

        for video in input_videos:
            compress_video(video, crf=default_crf)
        return

    # 3. Fallback: prompt user for a path
    target = input("Enter video path (or place video in the 'input' folder): ").strip().strip('"\'')
    if target:
        compress_video(target, crf=default_crf)
    else:
        print("No video file specified and no videos found in input folder.")


if __name__ == "__main__":
    main()
