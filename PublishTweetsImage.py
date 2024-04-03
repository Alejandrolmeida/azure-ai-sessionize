import os
import tweepy
from dotenv import load_dotenv
import random

# Load environment variables from a .env file
load_dotenv()

# Twitter API credentials
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET_KEY = os.getenv("TWITTER_API_SECRET_KEY")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Path to the image file
image_path = "bananas.jpg"

# Upload the image to Twitter and get the media ID
media = api.media_upload(image_path)
media_id = media.media_id_string

# Create a tweet with the text and the media ID
tweet = "¿Cuál es la altura de Mount Everest en términos de bananas? 🍌 Descúbrelo en mi último artículo. #Curiosidades #MountEverest"
status = api.update_status(status=tweet, media_ids=[media_id])

# Print the response from Twitter after posting the tweet
print(status)