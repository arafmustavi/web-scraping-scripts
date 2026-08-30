#!/usr/bin/env python3
"""
youtube_downloader.py
=====================
Download YouTube videos and/or audio and keep a local copy, based on a URL.

Two input modes (pick either one):
  1) Command-line argument(s):   pass one or more URLs directly with -u/--url
  2) CSV file:                   pass a CSV file with -i/--input (a column named
                                 'url' — falls back to the first column)

Engine: yt-dlp  (https://github.com/yt-dlp/yt-dlp)
Requires ffmpeg on PATH for MP4 merging and MP3 extraction.

Install dependencies:
    pip install yt-dlp
    # ffmpeg: https://ffmpeg.org/download.html  (or `apt install ffmpeg` / `brew install ffmpeg`)

Examples
--------
# Single video (best quality MP4)
python youtube_downloader.py -u "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Audio only (MP3) from one URL
python youtube_downloader.py -u "https://youtu.be/dQw4w9WgXcQ" -t audio

# Multiple URLs at once, capped at 1080p, into a custom folder
python youtube_downloader.py -u URL1 URL2 URL3 -q 1080 -o ./downloads

# Batch from a CSV file (column 'url'), both video AND audio
python youtube_downloader.py -i videos.csv -t both

Author: generated for arafmustavi/web-scraping-scripts
License: MIT (matches typical utility-script use)

NOTE ON USAGE: Only download content you own or have the right to download.
Respect YouTube's Terms of Service and applicable copyright law.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    sys.exit(
        "ERROR: yt-dlp is not installed.\n"
        "Install it with:  pip install yt-dlp\n"
        "(ffmpeg is also required for MP4 merging / MP3 extraction.)"
    )


# --------------------------------------------------------------------------- #
# Core download logic
# --------------------------------------------------------------------------- #
def build_ydl_opts(dl_type: str, quality: str, outdir: Path) -> dict:
    """Return a yt-dlp options dict for the requested download type/quality."""
    outdir.mkdir(parents=True, exist_ok=True)
    outtmpl = str(outdir / "%(uploader)s - %(title)s [%(id)s].%(ext)s")

    common = {
        "outtmpl": outtmpl,
        "noplaylist": False,        # allow playlists; set True to force single video
        "ignoreerrors": True,       # keep going if one item in a batch fails
        "quiet": False,
        "no_warnings": False,
        "restrictfilenames": True,  # safe filenames across OSes
        "concurrent_fragment_downloads": 4,
        "retries": 5,
    }

    if dl_type == "audio":
        # Extract best audio and convert to MP3
        common.update(
            {
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
            }
        )
    else:
        # Video (mp4). Cap height by requested quality; fall back gracefully.
        if quality == "best":
            fmt = "bestvideo*+bestaudio/best"
        else:
            fmt = (
                f"bestvideo[height<={quality}]+bestaudio/"
                f"best[height<={quality}]/best"
            )
        common.update(
            {
                "format": fmt,
                "merge_output_format": "mp4",
            }
        )

    return common


def download_one(url: str, dl_type: str, quality: str, outdir: Path) -> bool:
    """Download a single URL for the given type. Returns True on success."""
    # 'both' = run the video pass then the audio pass
    passes = ["video", "audio"] if dl_type == "both" else [dl_type]
    ok = True
    for p in passes:
        opts = build_ydl_opts(p, quality, outdir)
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ret = ydl.download([url])
                ok = ok and (ret == 0)
        except Exception as exc:  # noqa: BLE001 - report and continue
            print(f"  ! Failed ({p}) for {url}: {exc}", file=sys.stderr)
            ok = False
    return ok


# --------------------------------------------------------------------------- #
# Input handling
# --------------------------------------------------------------------------- #
def read_urls_from_csv(path: Path) -> list[str]:
    """Read URLs from a CSV. Prefer a 'url' column; else use the first column."""
    if not path.exists():
        sys.exit(f"ERROR: CSV file not found: {path}")

    urls: list[str] = []
    with path.open(newline="", encoding="utf-8-sig") as fh:
        sample = fh.read(2048)
        fh.seek(0)
        has_header = csv.Sniffer().has_header(sample) if sample.strip() else False

        if has_header:
            reader = csv.DictReader(fh)
            # find a 'url'-like column, case-insensitive
            url_key = next(
                (k for k in (reader.fieldnames or []) if k and k.strip().lower() == "url"),
                None,
            )
            for row in reader:
                val = (row.get(url_key) if url_key else next(iter(row.values()), "")) or ""
                val = val.strip()
                if val:
                    urls.append(val)
        else:
            for row in csv.reader(fh):
                if row and row[0].strip():
                    urls.append(row[0].strip())

    if not urls:
        sys.exit(f"ERROR: No URLs found in {path}")
    return urls


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download YouTube video/audio locally from URLs or a CSV file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument(
        "-u", "--url", nargs="+", metavar="URL",
        help="One or more YouTube URLs passed as arguments.",
    )
    src.add_argument(
        "-i", "--input", metavar="CSV",
        help="Path to a CSV file with a 'url' column (or URLs in the first column).",
    )
    parser.add_argument(
        "-t", "--type", choices=["video", "audio", "both"], default="video",
        help="What to download: video (mp4), audio (mp3), or both. Default: video.",
    )
    parser.add_argument(
        "-q", "--quality", default="best",
        help="Max video height, e.g. 2160, 1440, 1080, 720, 480, or 'best'. "
             "Ignored for audio. Default: best.",
    )
    parser.add_argument(
        "-o", "--output", default="downloads", metavar="DIR",
        help="Output directory. Default: ./downloads",
    )
    return parser.parse_args(argv)


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #
def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    urls = args.url if args.url else read_urls_from_csv(Path(args.input))
    outdir = Path(args.output)

    print(f"Queued {len(urls)} URL(s) | type={args.type} | quality={args.quality} "
          f"| output={outdir.resolve()}\n")

    successes = 0
    for idx, url in enumerate(urls, start=1):
        print(f"[{idx}/{len(urls)}] {url}")
        if download_one(url, args.type, str(args.quality), outdir):
            successes += 1
        print()

    failed = len(urls) - successes
    print(f"Done. {successes} succeeded, {failed} failed. Files in: {outdir.resolve()}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
