# ai-twitter-bot

An automated Twitter (X) assistant that fetches niche news, distills each article into tweet-sized summaries, de-duplicates previously posted content, and posts updates through the unofficial `tweety` client.

## ✨ Features
- **News Fetching:** Queries NewsAPI with configurable keywords and normalizes article metadata.
- **AI Summarisation:** Uses Hugging Face's BART pipeline to produce concise tweet candidates and score them by keyword relevance.
- **Duplicate Filtering:** Maintains a rolling history of published tweets to avoid reposting similar content.
- **Hands-Off Posting:** Logs into X via `tweety` and posts the selected tweets in sequence.
- **Local Persistence:** Stores the daily batch as well as the long-term tweet history on disk for auditing.

## 🧱 Architecture at a Glance
```
[Scheduler/manual run]
          |
          v
main.py ─▶ fetcher.fetch_news() ─▶ summarizer.summarize_article()
          |                                     |
          |                                     └─▶ score_summary()
          └─▶ storage.save_daily_tweets()
                    │
                    ├─▶ storage.filter_duplicates() ─▶ storage.save_tweets_to_history()
                    │
                    └─▶ tweeter.tweet_daily()
```

- **`config/config.py`** – Lists the niche keywords, article cap, and daily tweet count.
- **`fetcher.py`** – Builds the NewsAPI query and extracts title/description/URL triples.
- **`summarizer.py`** – Loads the BART summarisation pipeline and scores summaries by keyword hits.
- **`storage.py`** – Persists tweet history (`data/tweets.txt`) and the current batch (`data/daily_tweets.txt`).
- **`tweeter.py`** – Wraps `tweety.TweetClient` to log in and post each tweet with basic error handling.
- **`helper.py`** – Optional console helper for printing fetched articles during debugging.

## 📁 Project Structure
```
ai-twitter-bot/
├── architecture.txt          # Textual architecture overview
├── config/
│   └── config.py             # Keyword and limit configuration
├── data/
│   ├── daily_tweets.txt      # Current cycle’s tweets
│   └── tweets.txt            # Long-term tweet history
├── fetcher.py                # NewsAPI client
├── helper.py                 # Debug print helpers
├── main.py                   # Orchestrates the end-to-end workflow
├── requirements.txt          # Python dependencies
├── storage.py                # Disk persistence and deduplication helpers
├── summarizer.py             # Hugging Face summarisation pipeline
├── tweeter.py                # X/Twitter posting utilities
└── README.md
```

## 🚀 Getting Started
1. **Clone the repo**
    ```bash
    git clone https://github.com/ThePhoenix77/ai-twitter-bot.git
    cd ai-twitter-bot
    ```
2. **Install dependencies**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
3. **Create a `.env` file** in the project root:
    ```ini
    NEWS_API_KEY=your_newsapi_key
    TWITTER_USERNAME=your_username
    TWITTER_PASSWORD=your_password
    ```
    > `summarizer.py` will download the BART weights the first time it runs; keep the environment active until it completes.
4. **Review configuration** in `config/config.py` to adjust keywords, fetch limit, or number of tweets to publish per run.

## ▶️ Usage
- **Dry run (no posting):** Comment out the `tweet_daily` call in `main.py` to inspect the summaries first.
- **Full run:**
  ```bash
  python main.py
  ```
  The script fetches articles, prints the top-scoring summaries, saves them under `data/`, and posts any tweets that are not yet in the history file.

## 🔄 Future Enhancements
- Schedule hourly runs via cron, GitHub Actions, or another job runner.
- Add semantic similarity checks (e.g., embeddings) instead of keyword scoring alone.
- Expand to multiple niches by parameterising the configuration or loading from external files.
- Introduce richer logging or notifications for failures.

## 🤝 Contributing
Pull requests are welcome. Please run your changes locally and ensure `python main.py` completes without errors.

## 📄 License
MIT License.