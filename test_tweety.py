import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("X_API_KEY")
api_secret = os.getenv("X_API_KEY_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_secret = os.getenv("ACCESS_TOKEN_SECRET")

try:
    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_secret
    )

    # --- 3. Use the V2 method: client.create_tweet() ---
    response = client.create_tweet(text="tweet here")
    
    # You can inspect the response for details if needed
    print(f"Tweet successfully posted! ID: {response.data['id']}")
    
except Exception as e:
    print("Error:", e)

# print(f"{api_key} | {api_secret} | {access_token} | {access_secret}")