import requests
from datetime import datetime, timedelta
import telegram
import os

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

KEYWORDS = ['github', 'library', 'repo', 'tool', 'code']

def fetch_new_posts():
    url = "https://api.pushshift.io/reddit/search/submission/"
    yesterday = datetime.utcnow() - timedelta(days=1)
    params = {
        "subreddit": "MachineLearning",
        "sort": "desc",
        "sort_type": "created_utc",
        "after": int(yesterday.timestamp()),
        "size": 50,
    }
    r = requests.get(url, params=params)
    data = r.json().get('data', [])
    return data

def filter_relevant(posts):
    results = []
    for post in posts:
        title = post.get("title", "").lower()
        url = post.get("url", "")
        if any(k in title or k in url for k in KEYWORDS):
            results.append(f"- [{post.get('title')}]({url})")
    return results

def send_to_telegram(text):
    bot = telegram.Bot(token=BOT_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=text, parse_mode=telegram.ParseMode.MARKDOWN)

def run_bot():
    posts = fetch_new_posts()
    relevant = filter_relevant(posts)
    if relevant:
        today = datetime.utcnow().strftime("%d %B")
        text = f"🛰️ *AI Radar*: новые находки на Reddit /r/MachineLearning ({today})\n\n" + "\n".join(relevant)
        send_to_telegram(text)
    else:
        print("Нет релевантных постов")

if __name__ == "__main__":
    run_bot()
