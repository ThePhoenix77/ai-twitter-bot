import os
import re
from config import NICHE_KEYWORDS

from dotenv import load_dotenv
load_dotenv()


MODEL_NAME = os.getenv("HF_MODEL", "sshleifer/distilbart-cnn-12-6")

summarizer = None
try:
    from transformers import pipeline
    try:
        summarizer = pipeline("summarization", model=MODEL_NAME)
    except Exception as e:
        print(f"Warning: could not load Hugging Face model '{MODEL_NAME}': {e}")
        summarizer = None
except Exception as e:
    print(f"Warning: transformers library unavailable: {e}")
    summarizer = None


def score_summary(summary: str, keywords: list[str]) -> int:
    summary_lower = summary.lower()
    score = sum(1 for kw in keywords if kw.lower() in summary_lower)
    return score


def _fallback_summarize(text: str) -> str:
    """Lightweight fallback summarizer: prefer description sentences, truncate gracefully."""
    if not text:
        return ""
    t = re.sub(r"\s+", " ", text.strip())
    # Prefer full sentence under ~240 chars
    if len(t) <= 240:
        return t
    m = re.search(r"(.{120,240}?)[\.\!\?]\s", t)
    if m:
        return m.group(1).strip()
    # Otherwise truncate at last space
    return t[:240].rsplit(" ", 1)[0] + "..."


def summarize_article(title: str, description: str, url: str):
    summary_list = []
    model_input = f"{title}, {description or ''}".strip()
    if url:
        model_input += f" Read more: {url}"

    if summarizer is not None:
        try:
            summary = summarizer(
                model_input,
                max_length=min(max(len(model_input.split()) - 20, 60), 279),
                min_length=20,
                do_sample=False,
            )[0]["summary_text"]
        except Exception as e:
            print(f"warning: summarization failed at runtime, using fallback: {e}")
            summary = _fallback_summarize(description or title)
    else:
        summary = _fallback_summarize(description or title)

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
        