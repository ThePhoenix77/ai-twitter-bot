import os
import argparse
from fetcher import fetch_news
from summarizer import summarize_article
from storage import save_daily_tweets, filter_duplicates
from helper import file_empty_checker, print_article
from tweeter import tweeeter
from config import TWEET_COUNT
from dotenv import load_dotenv

load_dotenv()


def _format_final_tweet(summary: str, url: str) -> str:
    if not url:
        return summary
    return f"{summary}\n\n#news #AI #tips\n\n{url}"


def main(argv=None):
    parser = argparse.ArgumentParser(description="ai-twitter-bot runner")
    parser.add_argument("--dry-run", action="store_true", help="Run fetch+summarize and print previews without saving or posting.")
    parser.add_argument("--force", action="store_true", help="Force fetching even if daily_tweets.txt is not empty.")
    args = parser.parse_args(argv)

    should_fetch = args.force or file_empty_checker("data/daily_tweets.txt")

    if should_fetch:
        articles = fetch_news()
        print(f"Fetched {len(articles)} articles.\n")

        all_summaries = []
        for i, article in enumerate(articles, 1):
            title = article.get("title", "")
            description = article.get("description", "")
            url = article.get("url", "")
            print_article(article, i, title)

            summary_list = summarize_article(title, description, url)
            all_summaries.extend(summary_list)

        top_summaries = sorted(all_summaries, key=lambda x: x[1], reverse=True)[:TWEET_COUNT]
        unique_summaries = filter_duplicates(top_summaries)
        if not unique_summaries:
            print("No new tweets to schedule today; all candidates were duplicates.\n")

        if args.dry_run:
            print("\nDry run — previews of generated tweets (no save, no post):\n")
            for i, (summary, score, url) in enumerate(unique_summaries, 1):
                final = _format_final_tweet(summary, url)
                print(f" - Preview Tweet {i}: (Score: {score})\n--- {final}\n")
        else:
            save_daily_tweets(unique_summaries)
            for i, (summary, score, url) in enumerate(unique_summaries, 1):
                if url:
                    preview = f"{summary}\n{url}"
                else:
                    preview = summary
                print(f" - Tweet {i}: (Score: {score})\n--- {preview}")

    if args.dry_run:
        print("Dry run complete.")
    else:
        tweeeter()


if __name__ == "__main__":
    main()
