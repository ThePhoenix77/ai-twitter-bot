from fetcher import fetch_news
from summarizer import summarize_article
from dotenv import load_dotenv

load_dotenv()

def main():
    articles = fetch_news()
    print(f"Fetched {len(articles)} articles.\n")

    all_summaries = []
    for i, article in enumerate(articles, 1):
        title = article.get("title", "")
        description = article.get("description", "")
        url = article.get("url", "")

        summary_list = summarize_article(title, description, url)
        print(f" - Article {i}:")
        print(f" --- Title: {title} \n")
        print(f"{summary_list} \n")
        print("x+x+x+" * 18 + "\n")
        all_summaries.extend(summary_list)

    print(" - - -" * 18 + "\n")
    print(" * The top 3 tweets *\n")
    top_summaries = sorted(all_summaries, key=lambda x: x[1], reverse=True)[:3]
    for i, (summary, score) in enumerate(top_summaries, 1):
        print(f" - Tweet {i}: (Score: {score})\n--- {summary}")
    # print(top_summaries)

if __name__ == "__main__":
    main()
