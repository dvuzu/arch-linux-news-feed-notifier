import feedparser
import requests
import os

# RSS feed URL for Arch Linux News
RSS_FEED_URL = "https://archlinux.org/feeds/news/"

# Store the latest news ID in a local file
STATE_FILE = "latest_id"

# Discord Webhook URL (from repository secrets)
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

def get_latest_news_id():
    """Retrieve the latest news ID from the saved state."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return f.read()
    return None

def save_latest_news_id(latest_id):
    """Save the latest news ID to the state file."""
    with open(STATE_FILE, "w") as f:
        f.write(latest_id)

def fetch_arch_news():
    """Fetch Arch Linux RSS feed and return the latest entry."""
    feed = feedparser.parse(RSS_FEED_URL)
    if feed.entries:
        return feed.entries[0]  # Return the latest news entry
    return None

def send_discord_notification(title, link):
    """Send a notification to Discord via webhook."""
    content = f"@everyone New Arch Linux News: **{title}**\nRead more: {link}"
    payload = {"content": content}
    response = requests.post(DISCORD_WEBHOOK, json=payload)
    
    if response.status_code == 204:
        print("Notification sent successfully!")
    else:
        print(f"Failed to send notification. Status: {response.status_code}")

def main():
    latest_news = fetch_arch_news()
    if not latest_news:
        print("No news found.")
        return

    latest_id = latest_news.get("id", "")
    saved_id = get_latest_news_id()

    # If the latest news ID is different, send a notification
    if latest_id != saved_id:
        print(f"New news found: {latest_news['title']}")
        send_discord_notification(latest_news['title'], latest_news['link'])
        save_latest_news_id(latest_id)
    else:
        print("No new news.")

if __name__ == "__main__":
    main()
