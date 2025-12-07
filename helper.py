import os

def print_article(article, i, title):
    print(f" - Article {i}:")
    print(f" --- Title: {title} \n")
    print("x+x+x+" * 18 + "\n")

def print_articles(articles):
    if not articles:
        print("No articles found.")
        return

    for i, a in enumerate(articles, 1):
        print(f"\n--- Article {i} ---")
        print(f"Title: {a.get('title')}")
        print(f"Description: {a.get('description')}")
        print(f"URL: {a.get('url')}")
        print("-" * 40)

def file_empty_checker(path):
    return os.path.getsize(path) == 0