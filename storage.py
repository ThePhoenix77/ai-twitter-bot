import os
from datetime import datetime

TWEETS_FILE_PATH = "tweets.txt"

def load_tweets_history() -> set[str]:
    if not os.path.exists(TWEETS_FILE_PATH):
        return set()
    with open(TWEETS_FILE_PATH, "r", encoding = "utf-8") as f:
        return set(line.strip() for line in f.readlines() if not line.startswith('---') )

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

def filter_duplicates(daily_tweets: list[tuple[str, int]]) -> list[tuple[str, int]]:
    history = load_tweets_history()
    new_tweets = []

    for i, (summary, score) in enumerate(daily_tweets, start = 1):
        if summary not in history:
            new_tweets.append((summary, score))
            save_tweets_to_history(summary, i)
    return new_tweets

# def filter_duplicates(daily_tweets: list[str]) -> list[str]:
#     history = load_tweets_history()
#     new_tweets = []

#     for summary, score in daily_tweets:
#         if summary not in history:
#             new_tweets.append((summary, score))
#             save_tweets_to_history(summary)
#     return new_tweets