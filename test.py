import os
import tweepy
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Setup Tweepy client
client = tweepy.Client(
    consumer_key=os.getenv("API_KEY"),
    consumer_secret=os.getenv("API_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_SECRET")
)

# Your test tweet
test_message = "test :)"

try:
    response = client.create_tweet(text=test_message)
    print(f"✅ Tweet sent successfully! Tweet ID: {response.data['id']}")
except Exception as e:
    print(f"❌ Failed to send tweet. Error: {e}")
