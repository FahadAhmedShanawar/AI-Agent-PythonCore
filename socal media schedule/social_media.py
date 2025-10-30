import requests
import json
import os
from config import (
    TWITTER_BEARER_TOKEN, TWITTER_API_KEY, TWITTER_API_SECRET,
    TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET,
    META_ACCESS_TOKEN, META_PAGE_ID, META_INSTAGRAM_ACCOUNT_ID
)

def post_to_twitter(text, image_path=None, hashtags=None):
    """
    Post to Twitter using API v2.
    Requires Bearer Token and OAuth 1.0a for posting.
    """
    url = "https://api.twitter.com/2/tweets"
    headers = {
        "Authorization": f"Bearer {TWITTER_BEARER_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {"text": text}
    if hashtags:
        payload["text"] += " " + " ".join(["#" + h for h in hashtags])

    # For images, need to upload first (simplified, assuming no image for now)
    if image_path:
        # Twitter media upload requires separate API call
        # This is a placeholder; full implementation needed
        print(f"Twitter image upload not implemented yet. Image: {image_path}")

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print("Posted to Twitter successfully.")
        return True
    else:
        print(f"Failed to post to Twitter: {response.text}")
        return False

def post_to_facebook(text, image_path=None, hashtags=None):
    """
    Post to Facebook page using Graph API.
    """
    url = f"https://graph.facebook.com/v18.0/{META_PAGE_ID}/feed"
    params = {
        "access_token": META_ACCESS_TOKEN,
        "message": text
    }
    if hashtags:
        params["message"] += " " + " ".join(["#" + h for h in hashtags])

    if image_path:
        # For images, use /photos endpoint
        url = f"https://graph.facebook.com/v18.0/{META_PAGE_ID}/photos"
        files = {'source': open(image_path, 'rb')}
        response = requests.post(url, params=params, files=files)
    else:
        response = requests.post(url, params=params)

    if response.status_code == 200:
        print("Posted to Facebook successfully.")
        return True
    else:
        print(f"Failed to post to Facebook: {response.text}")
        return False

def post_to_instagram(text, image_path=None, hashtags=None):
    """
    Post to Instagram using Graph API.
    Requires image for Instagram posts.
    """
    if not image_path:
        print("Instagram requires an image.")
        return False

    # First, create media container
    url = f"https://graph.facebook.com/v18.0/{META_INSTAGRAM_ACCOUNT_ID}/media"
    params = {
        "access_token": META_ACCESS_TOKEN,
        "image_url": f"http://localhost:5000/{image_path}",  # Assuming local server
        "caption": text + (" " + " ".join(["#" + h for h in hashtags]) if hashtags else "")
    }

    response = requests.post(url, params=params)
    if response.status_code != 200:
        print(f"Failed to create Instagram media: {response.text}")
        return False

    media_id = response.json().get("id")

    # Publish the media
    publish_url = f"https://graph.facebook.com/v18.0/{META_INSTAGRAM_ACCOUNT_ID}/media_publish"
    publish_params = {
        "access_token": META_ACCESS_TOKEN,
        "creation_id": media_id
    }

    publish_response = requests.post(publish_url, params=publish_params)
    if publish_response.status_code == 200:
        print("Posted to Instagram successfully.")
        return True
    else:
        print(f"Failed to publish to Instagram: {publish_response.text}")
        return False

def post_to_platform(platform, text, image_path=None, hashtags=None):
    """
    Unified function to post to a specific platform.
    """
    if platform == "twitter":
        return post_to_twitter(text, image_path, hashtags)
    elif platform == "facebook":
        return post_to_facebook(text, image_path, hashtags)
    elif platform == "instagram":
        return post_to_instagram(text, image_path, hashtags)
    else:
        print(f"Unknown platform: {platform}")
        return False
