# YouTube Downloader

Download YouTube **videos** and/or **audio** and keep a local copy — either by
passing the URL as a command-line argument, or by listing URLs in a **CSV file**.

Built on [`yt-dlp`](https://github.com/yt-dlp/yt-dlp), the actively-maintained,
most reliable YouTube download engine.

## Setup

```bash
pip install -r requirements-youtube.txt
```

You also need **ffmpeg** on your PATH (used to merge video+audio into MP4 and to
extract MP3 audio):

| OS      | Install command |
|---------|-----------------|
| Windows | `winget install ffmpeg` |
| macOS   | `brew install ffmpeg` |
| Linux   | `sudo apt install ffmpeg` |

## Usage

### Mode 1 — pass URL(s) as arguments
```bash
# Single video (best quality MP4)
python youtube_downloader.py -u "https://www.youtube.com/watch?v=VIDEO_ID"

# Multiple URLs at once
python youtube_downloader.py -u URL1 URL2 URL3

# Audio only (MP3)
python youtube_downloader.py -u "https://youtu.be/VIDEO_ID" -t audio

# Cap resolution at 1080p into a custom folder
python youtube_downloader.py -u URL -q 1080 -o ./downloads
```

### Mode 2 — batch from a CSV file
Create a CSV with a `url` column (or just URLs in the first column):

```csv
url
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://youtu.be/9bZkp7q19f0
```

```bash
# Download every URL in the CSV as both video and audio
python youtube_downloader.py -i videos.csv -t both
```

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `-u`, `--url`     | one or more URLs      | —          | URLs passed directly (mutually exclusive with `-i`) |
| `-i`, `--input`   | path to CSV           | —          | CSV file of URLs (mutually exclusive with `-u`) |
| `-t`, `--type`    | `video` / `audio` / `both` | `video` | What to download |
| `-q`, `--quality` | `2160`/`1440`/`1080`/`720`/`480`/`best` | `best` | Max video height (ignored for audio) |
| `-o`, `--output`  | directory             | `downloads`| Where files are saved |

Files are named `Uploader - Title [id].ext` and saved to the output folder.
Batch jobs continue even if one item fails, and the script reports a
success/failure summary at the end.

## Notes
- Playlists are supported (a playlist URL downloads all its items).
- Only download content you own or have the right to download. Respect
  YouTube's Terms of Service and applicable copyright law.
