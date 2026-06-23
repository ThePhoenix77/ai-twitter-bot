import os
import json
import urllib.error
import urllib.request

from dotenv import load_dotenv

load_dotenv()

DEFAULT_XQUIK_API_BASE = "https://xquik.com/api/v1"


def load_backend():
    backend = os.getenv("TWITTER_BACKEND", "").strip().lower()
    return backend or "tweepy"


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
            "Failure to auth.\nError: missing Twitter credential in the env variables: "
            + ", ".join(missing)
        )

    return api_key, api_secret, access_token, access_secret


def load_xquik_credentials():
    api_key = os.getenv("XQUIK_API_KEY")
    account = os.getenv("XQUIK_ACCOUNT")
    api_base = (
        os.getenv("XQUIK_API_BASE", "").strip().rstrip("/")
        or DEFAULT_XQUIK_API_BASE
    )

    missing = [
        name
        for name, value in (
            ("XQUIK_API_KEY", api_key),
            ("XQUIK_ACCOUNT", account),
        )
        if not value
    ]

    if missing:
        raise RuntimeError(
            "Failure to auth.\nError: missing Xquik credential in the env variables: "
            + ", ".join(missing)
        )

    return api_key, account, api_base


def build_client():
    import tweepy

    api_key, api_secret, access_token, access_secret = load_credentials()
    return tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_secret,
    )


def format_final_tweet(raw_entry):
    if " || " in raw_entry:
        summary, url = raw_entry.split(" || ", 1)
        summary = summary.strip()
        url = url.strip()
    else:
        summary, url = raw_entry, ""

    return summary if not url else f"{summary}\n\n#news #AI #tips\n\n{url}"


def post_with_tweepy(final_tweet):
    client = build_client()
    response = client.create_tweet(text=final_tweet)
    tweet_id = response.data.get("id") if response and response.data else "?"
    return {"backend": "tweepy", "id": tweet_id}


def post_with_xquik(final_tweet):
    api_key, account, api_base = load_xquik_credentials()
    payload = json.dumps({"account": account, "text": final_tweet}).encode("utf-8")
    request = urllib.request.Request(
        f"{api_base}/x/tweets",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "X-API-Key": api_key,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            response_body = response.read().decode("utf-8")
            status = response.status
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"Xquik post failed with HTTP {error.code}: {detail}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"Xquik post failed: {error.reason}") from error

    if status not in (200, 202):
        raise RuntimeError(f"Xquik post failed with HTTP {status}: {response_body[:500]}")

    body = json.loads(response_body) if response_body else {}
    return {"backend": "xquik", "status": status, "body": body}


def extract_xquik_identifier(body):
    if not isinstance(body, dict):
        return None

    for key in ("tweetId", "id", "writeActionId"):
        value = body.get(key)
        if value:
            return value

    data = body.get("data")
    if isinstance(data, dict):
        for key in ("tweetId", "id", "writeActionId"):
            value = data.get(key)
            if value:
                return value

    return None


def post_tweet(final_tweet):
    backend = load_backend()
    if backend == "xquik":
        return post_with_xquik(final_tweet)
    if backend in ("tweepy", "twitter", "x"):
        return post_with_tweepy(final_tweet)
    raise RuntimeError("Unsupported TWITTER_BACKEND. Use tweepy or xquik.")


def format_post_result(result):
    if result["backend"] == "xquik":
        status_word = "accepted" if result["status"] == 202 else "sent"
        identifier = extract_xquik_identifier(result["body"])
        if identifier:
            return f"Tweet {status_word} with Xquik. ID: {identifier}\n"
        return f"Tweet {status_word} with Xquik.\n"

    return f"Tweet sent successfully. ID: {result['id']}\n"


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
        final_tweet = format_final_tweet(raw_entry)
        result = post_tweet(final_tweet)
        print(format_post_result(result))
    except Exception as e:
        print(f"Failure to tweet.\nError: {e}")
