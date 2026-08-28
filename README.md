# Web Scraping Scripts

A collection of Python scripts for web scraping, data extraction, and automation tasks.

The repository currently includes **Instagram utilities built with [Instaloader](https://instaloader.github.io/)**, with additional scraping tools planned.

## Project Structure

```text
web-scraping-scripts/
│
├── instagram/
│   └── download-insta-profiles.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Requirements

* Python 3.9+
* Git
* An Instagram account for authenticated Instaloader operations
* A virtual environment is recommended

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/web-scraping-scripts.git
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

If `requirements.txt` does not exist yet:

```bash
pip install instaloader
pip freeze > requirements.txt
```

## Instagram Profile Downloader

The Instagram utility uses Instaloader to download publicly accessible posts/media associated with an Instagram profile.

### Basic Usage

```bash
python .\instagram\download-insta-profiles.py <instagram_username>
```

Example:

```powershell
python .\instagram\download-insta-profiles.py iamsrk
```

The downloaded content will be stored locally by Instaloader.

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

## Development

Create a new virtual environment and install dependencies:

```bash
python -m venv .venv
```

```powershell
.\.venv\Scripts\Activate.ps1
```

```bash
pip install -r requirements.txt
```

Run the Instagram downloader:

```powershell
python .\instagram\download-insta-profiles.py <username>
```

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
