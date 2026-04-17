# ai-twitter-bot

An automated Twitter (X) assistant that fetches niche news, distills each article into tweet sized summaries and posts the tweets on your behalf.
You can check my X account [seabasszealot](https://x.com/seabasszealot), being ran by it.

## Features
- **Automated posting:** This project uses github workflow and github actions to schedule the posts hourly or so(personal choice), you can modify it to your taste by changeing the TWEET_COUNT in config.py and updating the cron in tweet.yml to your choice.
- **News Fetching:** Queries NewsAPI with configurable keywords and normalizes article metadata.
- **AI Summarisation:** Uses Hugging Face's BART pipeline to produce concise tweet candidates and score them by keyword relevance.
- **Hands-Off Posting:** Logs on your behalf into your X (Twitter) account and posts the selected tweets in sequence.
- **Local Persistence:** Stores the daily batch as well as the long-term tweet history on disk for auditing.
- **Duplicates filtering:** Each tweet is unique, as the X (Twitter) imposes so the account isn't considered a bot and can longer tweet as necessary.

## Architecture at a Glance
```
[Scheduler/manual run]
          |
          v
main.py ─▶ fetcher.fetch_news() ─▶ summarizer.summarize_article()
          |                                     |
          |                                     └─▶ score_summary()
          └─▶ storage.save_daily_tweets()
                    │
                    ├─▶ storage.filter_duplicates()    └─▶ storage.save_tweets_to_history()
                    │
                    └─▶ tweeter.tweet_daily()
```

- **`config/config.py`** – Lists the niche keywords, article cap, and daily tweet count.
- **`fetcher.py`** – Builds the NewsAPI query and extracts title/description/URL triples.
- **`summarizer.py`** – Loads the BART summarisation pipeline and scores summaries by keyword hits.
- **`storage.py`** – Persists tweet history (`data/tweets.txt`) and the current batch (`data/daily_tweets.txt`).
- **`tweeter.py`** – Wraps `tweety.TweetClient` to log in and post each tweet with basic error handling.
- **`helper.py`** – Optional console helper for printing fetched articles during debugging.

## Project Structure
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

## Getting Started
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
    X_API_KEY=your_x_api_key
    X_API_KEY_SECRET=your_x_api_key_secret
    ACCESS_TOKEN=your_x_access_token
    ACCESS_TOKEN_SECRET=your_x_access_token_secret
    ```
    > `summarizer.py` will download the BART weights the first time it runs; keep the environment active until it completes.
4. **Review configuration** in `config/config.py` to adjust keywords, fetch limit, or number of tweets to publish per run.

## Usage
- **Dry run (no posting):** Comment out the `tweet_daily` call in `main.py` to inspect the summaries first.
- **Full run:**
  ```bash
  python3.11 main.py
  ```
  The script fetches articles, prints the top scoring summaries, saves them under `data/`, and posts any tweets that are not yet in the history file.

## Future Enhancements.
- Adding semantic similarity checks (e.g., embeddings) instead of keyword scoring alone.
- Expanding to multiple niches by parameterising the configuration or loading from external files.
- Introducing richer logging or notifications for failures.

## Contributing
Pull requests are welcome. Please run your changes locally and ensure `python main.py` completes without errors.

## License
MIT License.
