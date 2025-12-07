import os
from fetcher import fetch_news
from config import NICHE_KEYWORDS

from dotenv import load_dotenv
load_dotenv()

from transformers import pipeline
summarizer = pipeline("summarization", model = "facebook/bart-large-cnn")

def score_summary(summary: str, keywords: list[str]) -> int:
    summary_lower = summary.lower()
    score = sum(1 for kw in keywords if kw.lower() in summary_lower)
    return score

def summarize_article(title: str, description: str, url: str):
    summary_list = []
    model_input = f"{title}, {description}"
    if url:
        model_input += f"Read more: {url}"
    
    summary = summarizer(
        model_input,
        max_length=min(max(len(model_input.split()) - 20, 60), 279),
        min_length=20,
        do_sample=False,
    )[0]["summary_text"]
    score = score_summary(summary, NICHE_KEYWORDS)
    return [(summary, score, url)]


# OpenAI trial(not free w9)
# openai_api_key = os.getenv("OPENAI_API_KEY")
# # print(" * OpenAI API key: ", openai_api_key)
# client = OpenAI(api_key = openai_api_key)
# prompt = f"Generate {max_variations} short, educational tweets based on the following article in a friendly conversational style. Keep each tweet under 280 characters. Article: {model_input}"
# response = client.chat.completions.create(model = "gpt-4o-mini", messages=[{"role": "system", "content": "You are a helpful assistant that creates the best short engaging news tweets."},
#                                                                            {"role": "user", "content": prompt}])
# model_output = response.choices[0].message.content
# tweets = [line.strip("_- .•0123456789") for line in model_output.split("\n") if line.strip()]
# return tweets[:max_variations]
        