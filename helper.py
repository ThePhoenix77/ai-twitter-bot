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