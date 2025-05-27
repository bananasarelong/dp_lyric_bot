import json
import os
import random
import tweepy
from dotenv import load_dotenv

load_dotenv()  # Load secrets from .env

# Twitter API setup
client = tweepy.Client(
    consumer_key=os.getenv("API_KEY"),
    consumer_secret=os.getenv("API_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_SECRET")
)

def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def get_unused_lyrics():
    all_lyrics = load_json('lyrics.json')
    try:
        used_lyrics = load_json('used_lyrics.json')
    except FileNotFoundError:
        used_lyrics = []

    unused = [lyric for lyric in all_lyrics if lyric not in used_lyrics]
    return all_lyrics, used_lyrics, unused

def select_lyric():
    all_lyrics, used_lyrics, unused = get_unused_lyrics()
    if not unused:
        used_lyrics = []
        unused = all_lyrics[:]
        print("🔁 All lyrics used — resetting list.")

    random.shuffle(unused)  # Shuffle the remaining unused list
    chosen = unused[0]
    used_lyrics.append(chosen)
    save_json('used_lyrics.json', used_lyrics)
    return chosen

def tweet_lyric(text):
    try:
        client.create_tweet(text=text)
        print(f"✅ Tweeted:\n{text}")
    except Exception as e:
        print(f"❌ Error tweeting: {e}")
        if hasattr(e, 'response') and e.response is not None:
            headers = e.response.headers
            rate_limit = headers.get('x-rate-limit-limit')
            rate_remaining = headers.get('x-rate-limit-remaining')
            rate_reset = headers.get('x-rate-limit-reset')
            print(f"Rate limit info (error response): limit={rate_limit}, remaining={rate_remaining}, reset={rate_reset}")
        else:
            print("No rate limit info available in error response.")

if __name__ == "__main__":
    lyric = select_lyric()
    tweet_lyric(lyric)
