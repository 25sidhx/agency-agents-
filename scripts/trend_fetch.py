#!/usr/bin/env python3
"""
Fetch recent Nagpur tweets via twitterapi.io and output a digest.
"""
import os
import json
import urllib.request
import urllib.parse
from datetime import datetime

def load_env():
    """Load key=value from ~/.hermes/.env"""
    env_path = os.path.expanduser('~/.hermes/.env')
    env = {}
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    k, v = line.split('=', 1)
                    env[k] = v.strip('"\'')
    return env

def fetch_tweets(api_key, query="Nagpur", count=50):
    url = "https://api.twitterapi.io/1.1/search/tweets.json"
    params = {
        'q': query,
        'count': count,
        'result_type': 'recent',
        'tweet_mode': 'extended'
    }
    query_string = urllib.parse.urlencode(params)
    full_url = f"{url}?{query_string}"
    req = urllib.request.Request(full_url, headers={'X-API-Key': api_key})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.load(resp)
            return data.get('statuses', [])
    except Exception as e:
        print(f"ERROR fetching tweets: {e}")
        return []

def format_digest(tweets):
    if not tweets:
        return "No tweets found for Nagpur."
    # Engagement: likes + retweets + replies (if available)
    def engagement(t):
        fav = t.get('favorite_count', 0)
        rt = t.get('retweet_count', 0)
        rep = t.get('reply_count', 0)
        return fav + rt + rep
    sorted_tweets = sorted(tweets, key=engagement, reverse=True)
    top = sorted_tweets[:5]
    lines = []
    lines.append(f"🐦 Nagpur Twitter Trends — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"Total recent tweets: {len(tweets)}")
    lines.append("\n**Top tweets by engagement:**")
    for i, t in enumerate(top, 1):
        user = t['user']['screen_name']
        text = t['full_text'].replace('\n', ' ').strip()
        if len(text) > 120:
            text = text[:117] + "..."
        fav = t.get('favorite_count', 0)
        rt = t.get('retweet_count', 0)
        rep = t.get('reply_count', 0)
        lines.append(f"{i}. @{user} (❤️{fav} 🔄{rt} 💬{rep}): {text}")
    # Hashtags
    hashtags = {}
    for t in tweets:
        for tag in t.get('entities', {}).get('hashtags', []):
            tag_text = tag['text'].lower()
            hashtags[tag_text] = hashtags.get(tag_text, 0) + 1
    top_tags = sorted(hashtags.items(), key=lambda x: x[1], reverse=True)[:5]
    if top_tags:
        lines.append("\n**Top hashtags:**")
        for tag, cnt in top_tags:
            lines.append(f"#{tag} ({cnt})")
    return "\n".join(lines)

def main():
    env = load_env()
    api_key = env.get('TWITTER_API_KEY')
    if not api_key:
        print("ERROR: TWITTER_API_KEY not set in ~/.hermes/.env")
        return
    tweets = fetch_tweets(api_key, query="Nagpur OR #Nagpur OR Nagpur news", count=100)
    digest = format_digest(tweets)
    print(digest)

if __name__ == "__main__":
    main()