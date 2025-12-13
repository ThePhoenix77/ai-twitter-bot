import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

def load_credentials():
    api_key = os.getenv("X_API_KEY")
    api_secret = os.getenv("X_API_KEY_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_secret = os.getenv("ACCESS_TOKEN_SECRET")

    missing = [
        name
        for name, value in (
            ("X_API_KEY", api_key),
            ("X_API_KEY_SECRET", api_secret),
            ("ACCESS_TOKEN", access_token),
            ("ACCESS_TOKEN_SECRET", access_secret),
        )
        if not value
    ]

    if missing:
        raise RuntimeError(
            "Failure to auth.\nError: missing twitter credential in the env variables: "
            + ", ".join(missing)
        )

    return api_key, api_secret, access_token, access_secret

def build_client():
    api_key, api_secret, access_token, access_secret = load_credentials()
    return tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_secret,
    )

def tweeeter():
    with open("data/daily_tweets.txt", "r", encoding="utf-8") as f:
        lines = [line for line in f.readlines() if line.strip()]

    if not lines:
        print("No tweets queued in data/daily_tweets.txt. Add entries and retry.\n")
        return

    raw_entry = lines[0].strip()
    remaining_tweets = lines[1:]

    with open("data/daily_tweets.txt", "w", encoding="utf-8") as f:
        f.writelines(remaining_tweets)
    try:
        client = build_client()
        if " || " in raw_entry:
            summary, url = raw_entry.split(" || ", 1)
            summary = summary.strip()
            url = url.strip()
        else:
            summary, url = raw_entry, ""

        final_tweet = summary if not url else f"{summary}\n\n#news #AI #tips\n\n{url}"
        response = client.create_tweet(text=final_tweet)
        tweet_id = response.data.get("id") if response and response.data else "?"
        print(f"Tweet sent successfully. ID: {tweet_id}\n")
    except Exception as e:
        print(f"Failure to tweet.\nError: {e}")
