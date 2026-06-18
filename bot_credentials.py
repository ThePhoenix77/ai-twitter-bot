# only use this script to generate the automated bot account's ACCESS_TOKEN and ACCESS_TOKEN_SECRET credentials
# in case you want to separate your main account from your automated one

import tweepy

API_KEY = "your-main-account-api-key"
API_SECRET = "your-main-account-api-key-secret"

# 1. Create handler
auth = tweepy.OAuth1UserHandler(
    API_KEY,
    API_SECRET,
    callback="http://localhost:8000/callback"
)

# 2. STEP REQUIRED: generate request token
auth_url = auth.get_authorization_url()
print("Go here and authorize:", auth_url)

# 3. Paste verifier AFTER authorization
verifier = input("Paste oauth_verifier: ")

# 4. Exchange for access tokens
access_token, access_token_secret = auth.get_access_token(verifier)

print("ACCESS TOKEN:", access_token)
print("ACCESS TOKEN SECRET:", access_token_secret)

