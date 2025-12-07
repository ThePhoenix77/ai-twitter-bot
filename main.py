import os
from fetcher import fetch_news
from summarizer import summarize_article
from storage import save_daily_tweets
from helper import file_empty_checker, print_article
from tweeter import tweeeter
from config import TWEET_COUNT
from dotenv import load_dotenv

load_dotenv()

def main():
    if file_empty_checker("data/daily_tweets.txt"):
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
        save_daily_tweets(top_summaries)
        for i, (summary, score, url) in enumerate(top_summaries, 1):
            if url:
                preview = f"{summary}\n{url}"
            else:
                preview = summary
            print(f" - Tweet {i}: (Score: {score})\n--- {preview}")
    
    tweeeter()

if __name__ == "__main__":
    main()
