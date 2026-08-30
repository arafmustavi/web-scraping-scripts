# Web Scraping Scripts

A collection of Python scripts for web scraping, data extraction, and automation tasks.


## Project Structure

```text
web-scraping-scripts/
│
├── instagram/
│   └── download-insta-profiles.py
├── youtube/
│   └── download-yt-videos.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Instagram
includes **Instagram utilities built with [Instaloader](https://instaloader.github.io/)**, with additional scraping tools planned.

## YouTube 

Download YouTube **videos** and/or **audio** and keep a local copy — either by
passing the URL as a command-line argument, or by listing URLs in a **CSV file**.

Built on [`yt-dlp`](https://github.com/yt-dlp/yt-dlp), the actively-maintained,
most reliable YouTube download engine.



## Requirements
mentioned details in the requirements.txt

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/arafmustavi/web-scraping-scripts.git
cd web-scraping-scripts
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

You also need **ffmpeg** on your PATH (used to merge video+audio into MP4 and to
extract MP3 audio):

| OS      | Install command |
|---------|-----------------|
| Windows | `winget install ffmpeg` |
| macOS   | `brew install ffmpeg` |
| Linux   | `sudo apt install ffmpeg` |

## Usage


## Instagram

The Instagram utility uses Instaloader to download publicly accessible posts/media associated with an Instagram profile.

```bash
python .\instagram\download-insta-profiles.py <instagram_username>
```

Example:

```powershell
python .\instagram\download-insta-profiles.py iamsrk
```

The downloaded content will be stored locally by Instaloader.


## Youtube

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

--------
## Instagram Authentication

Some Instagram content may require authentication.

Instead of logging in with your username and password every time the script runs, it is recommended to use an **Instaloader session**.

Create a session once:

```bash
instaloader --login=<your_instagram_username>
```

Instaloader will prompt you for your password and create a local session.

The Python script can then load the saved session:

```python
loader.load_session_from_file("<your_instagram_username>")
```

### Why use sessions?

Using a saved session avoids repeatedly sending username/password login requests and is generally preferable for local automation.

## Security

**Never commit credentials or authentication sessions to GitHub.**

Add the following to `.gitignore`:

```gitignore
# Virtual environment
.venv/

# Python
__pycache__/
*.py[cod]

# Environment variables
.env

# Instaloader sessions
*.session

# IDE
.vscode/
.idea/
```

If credentials or session files are accidentally committed, revoke/rotate the affected credentials and remove the sensitive data from the repository history.


## Planned Scripts

The repository is intended to grow into a collection of reusable scraping and automation scripts.

Potential additions:

* [ ] Instagram profile downloader
* [ ] Instagram post downloader
* [ ] Instagram hashtag utilities
* [ ] Instagram metadata extraction
* [ ] Generic webpage scraper
* [ ] Link extractor
* [ ] Image URL extractor
* [ ] CSV/JSON data export
* [ ] Scheduled scraping jobs
* [ ] Docker support
* [ ] Logging and error handling

## Disclaimer

This project is intended for **educational and personal automation purposes**.

When using these scripts, respect:

* Instagram's Terms of Use and applicable policies
* Website `robots.txt` and access restrictions where applicable
* Copyright and intellectual-property rights
* Privacy and applicable data-protection laws
* Rate limits and service restrictions

Do not use the scripts to access private accounts or data that you are not authorized to access.

## License

This project is currently intended for personal/educational use.

If you decide to publish it as an open-source project, add an appropriate license such as MIT:

```text
MIT License
```

---

## Author

**Araf Mustavi**

GitHub: `https://github.com/arafmustavi`
