import os
from datetime import datetime

TWEETS_FILE_PATH = "data/tweets.txt"
DAILY_TWEETS_FILE_PATH = "data/daily_tweets.txt"

def load_tweets_history() -> set[str]:
    if not os.path.exists(TWEETS_FILE_PATH):
        return set()

    history: set[str] = set()
    with open(TWEETS_FILE_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("---"):
                continue
            stripped = line.strip()
            if not stripped:
                continue
            if ". " in stripped:
                _, summary = stripped.split(". ", 1)
            else:
                summary = stripped
            history.add(summary)
    return history

def save_tweets_to_history(tweet: str, index: int):
    today = datetime.now().strftime("%d/%m/%Y")
    day_header = f"--- {today} ---\n"

    if os.path.exists(TWEETS_FILE_PATH):
        with open(TWEETS_FILE_PATH, "r", encoding = "utf-8") as f:
            content = f.read()
    else:
        content = ""
    with open(TWEETS_FILE_PATH, "a", encoding = "utf-8") as f:
        if day_header not in content:
            f.write(day_header)
        f.write(f"{index}. {tweet.strip()}\n")
        # f.write(index + ". " + tweet.strip() + "\n")

def save_daily_tweets(daily_tweets: list[tuple[str, int, str]]):
    with open(DAILY_TWEETS_FILE_PATH, "w", encoding="utf-8") as f:
        for summary, score, url in daily_tweets:
            summary_clean = summary.strip()
            url_clean = (url or "").strip()
            if url_clean:
                line = f"{summary_clean} || {url_clean}"
            else:
                line = summary_clean
            f.write(f"{line}\n")

def filter_duplicates(daily_tweets: list[tuple[str, int, str]]) -> list[tuple[str, int, str]]:
    history = load_tweets_history()
    new_tweets: list[tuple[str, int, str]] = []
    seen_today: set[str] = set()

    for summary, score, url in daily_tweets:
        summary_clean = summary.strip()

        if summary_clean in history or summary_clean in seen_today:
            continue

        new_tweets.append((summary, score, url))
        seen_today.add(summary_clean)
        save_tweets_to_history(summary_clean, len(seen_today))

    return new_tweets
