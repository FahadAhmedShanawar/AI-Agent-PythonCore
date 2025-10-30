import json
import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from social_media import post_to_platform

POSTS_FILE = 'posts.json'

def load_posts():
    try:
        with open(POSTS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_posts(posts):
    with open(POSTS_FILE, 'w') as f:
        json.dump(posts, f, indent=4)

def check_and_post():
    posts = load_posts()
    current_time = datetime.now()
    to_remove = []

    for i, post in enumerate(posts):
        scheduled_time = datetime.fromisoformat(post['scheduled_time'])
        if current_time >= scheduled_time:
            success = post_to_platform(
                post['platform'],
                post['text'],
                post.get('image_path'),
                post.get('hashtags')
            )
            if success:
                print(f"Posted: {post['text']} to {post['platform']}")
            else:
                print(f"Failed to post: {post['text']} to {post['platform']}")
            to_remove.append(i)

    # Remove posted items (in reverse order to avoid index issues)
    for i in reversed(to_remove):
        del posts[i]

    save_posts(posts)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_and_post, 'interval', seconds=60)  # Check every minute
    scheduler.start()
    print("Scheduler started. Checking for posts every minute.")
    return scheduler
