from fetcher import fetch_news
from summarizer import summarize_article
from dotenv import load_dotenv

load_dotenv()

def main():
    articles = fetch_news()
    print(f"Fetched {len(articles)} articles.\n")

    for i, article in enumerate(articles, 1):
        title = article.get("title", "")
        description = article.get("description", "")
        url = article.get("url", "")

        summary_list = summarize_article(title, description, url)
        print(f" - Article {i}:")
        print(f" --- Title: {title} \n")
        print(f"{summary_list} \n")
        print("x+x+x+" * 18 + "\n")

if __name__ == "__main__":
    main()
