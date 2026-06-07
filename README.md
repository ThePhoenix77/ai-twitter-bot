# ai-twitter-bot

<img width="1197" height="718" alt="ai-twitter-bot" src="https://github.com/user-attachments/assets/e47f7ebf-abe4-46a7-afa0-2acef9281ac7" />

`ai-twitter-bot` is an automated Twitter (X) assistant that fetches niche news, distills each article into tweet sized summaries and posts the tweets on your behalf.
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

   You can get your API keys and credentials of the news API from [newsapi.org](https://newsapi.org/) and Twitter/X from [docs.x.com/x-api](https://docs.x.com/x-api/overview).
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

## Pairing with GetXAPI for Cheaper Read Operations (Optional)

For users who need a cheaper or higher-rate-limit option for read-only Twitter (X) operations such as tweet search, profile lookup, and follower lists, this project can be paired with [GetXAPI](https://getxapi.com), a budget Twitter / X data API priced at $0.05 per 1K tweets versus the official X API basic tier at $200 / month.

Two integration patterns:

1. **Run side-by-side in your AI client.** Keep this project for its primary workflow and add the [official GetXAPI MCP server](https://github.com/getxapi/getxapi-mcp) for read-heavy tasks. Each tool name routes to the backend best suited for that operation.

2. **Add a backend toggle.** For a code-level reference of an optional alternative backend behind a single env variable, see the [PR pattern merged into a sibling project](https://github.com/GenAIwithMS/twitter-mcp/pull/3).

GetXAPI quick start:

- Signup with $0.50 free credit (no card required): https://getxapi.com/signup
- Official GetXAPI MCP server: https://github.com/getxapi/getxapi-mcp
- npm: `@getxapi/mcp`
- Pay-per-call pricing: $0.001 / call, $0.05 / 1K tweets

This pairing is fully optional. No behavior change for existing users.

## License
MIT License.
