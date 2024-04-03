import os
import tweepy
import schedule
import time
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Configuración de credenciales para la API de Twitter
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET_KEY = os.getenv("TWITTER_API_SECRET_KEY")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# Authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Inicializa el cliente de tweepy con tus credenciales de Twitter
client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN,
                       consumer_key=TWITTER_API_KEY,
                       consumer_secret=TWITTER_API_SECRET_KEY,
                       access_token=TWITTER_ACCESS_TOKEN,
                       access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
                       wait_on_rate_limit=True)

# Load the tweets from the JSON file
tweets = []
with open('Tweets.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header
    for row in reader:
        tweets.append({'Fecha': row[0], 'Hora': row[1], 'Mensaje': row[2]})  # Assuming date is in first column, time in second, and text in third

# Function to post a tweet
def post_tweet(tweet):
    client.create_tweet(text=tweet['Mensaje'])

# Schedule the tweets
for tweet in tweets:
    # Parse the date and time
    date = datetime.strptime(tweet['Fecha'], '%d-%m-%Y').date()
    tweet_time = datetime.strptime(tweet['Hora'], '%I:%M %p').time()

    # Get the day of the week
    day_of_week = date.strftime('%A').lower()

    # Schedule the tweet
    getattr(schedule.every(), day_of_week).at(tweet_time.strftime('%H:%M')).do(post_tweet, tweet)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)