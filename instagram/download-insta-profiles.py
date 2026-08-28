import argparse
import instaloader
import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("INSTAGRAM_USERNAME")
password = os.getenv("INSTAGRAM_PASSWORD")


def download_profile(username: str):
    loader = instaloader.Instaloader()
    loader.login(username, password)


    profile = instaloader.Profile.from_username(
        loader.context,
        username
    )

    loader.download_profile(
        profile,
        profile_pic=False
    )


def main():
    parser = argparse.ArgumentParser(
        description="Download publicly accessible Instagram profile posts."
    )

    parser.add_argument(
        "username",
        help="Instagram username"
    )

    args = parser.parse_args()

    download_profile(args.username)


if __name__ == "__main__":
    main()