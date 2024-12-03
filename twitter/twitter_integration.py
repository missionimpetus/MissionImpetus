import tweepy
import logging
import time
import re
import pandas as pd
from textblob import TextBlob
from datetime import datetime
from collections import Counter

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# OAuth2 Authentication for Tweepy
def authenticate_twitter():
    """
    Authenticate with Twitter API using OAuth.
    """
    logging.info("Authenticating with Twitter API...")
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    
    api = tweepy.API(auth, wait_on_rate_limit=True)
    
    if not api.verify_credentials():
        logging.error("Authentication failed.")
        return None
    logging.info("Authentication successful.")
    return api


# Tweet posting function
def post_tweet(api, message):
    """
    Post a tweet to the authenticated Twitter account.
    """
    logging.info(f"Posting tweet: {message}")
    try:
        api.update_status(message)
        logging.info("Tweet posted successfully.")
    except tweepy.TweepError as e:
        logging.error(f"Error posting tweet: {e}")


# Fetch user timeline tweets
def fetch_user_timeline(api, user_handle, count=100):
    """
    Fetch the latest tweets from a user's timeline.
    """
    logging.info(f"Fetching tweets from @{user_handle}...")
    try:
        tweets = api.user_timeline(screen_name=user_handle, count=count, tweet_mode="extended")
        logging.info(f"Fetched {len(tweets)} tweets from @{user_handle}.")
        return tweets
    except tweepy.TweepError as e:
        logging.error(f"Error fetching user timeline: {e}")
        return []


# Extract tweet content and time
def extract_tweet_data(tweets):
    """
    Extract relevant information from the tweets.
    """
    tweet_data = []
    for tweet in tweets:
        tweet_info = {
            "id": tweet.id,
            "created_at": tweet.created_at,
            "text": tweet.full_text,
            "likes": tweet.favorite_count,
            "retweets": tweet.retweet_count
        }
        tweet_data.append(tweet_info)
    return tweet_data


# Analyze tweet sentiment
def analyze_sentiment(tweet_text):
    """
    Analyze sentiment of the tweet using TextBlob.
    """
    blob = TextBlob(tweet_text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0:
        return "positive"
    elif sentiment < 0:
        return "negative"
    else:
        return "neutral"


# Perform sentiment analysis on a set of tweets
def analyze_tweets_sentiment(tweets):
    """
    Analyze sentiment for a batch of tweets and store the results.
    """
    logging.info("Analyzing sentiment for tweets...")
    sentiments = []
    for tweet in tweets:
        sentiment = analyze_sentiment(tweet["text"])
        sentiments.append(sentiment)
    sentiment_count = Counter(sentiments)
    logging.info(f"Sentiment Analysis - Positive: {sentiment_count['positive']}, Negative: {sentiment_count['negative']}, Neutral: {sentiment_count['neutral']}")
    return sentiment_count


# Fetch and analyze trends for a specific location (WOEID)
def fetch_trends(api, woeid):
    """
    Fetch trending topics for a given location based on WOEID.
    """
    logging.info(f"Fetching trending topics for WOEID {woeid}...")
    try:
        trends = api.trends_place(woeid)
        trend_data = [trend['name'] for trend in trends[0]['trends']]
        logging.info(f"Trending topics: {trend_data[:5]}")  # Display top 5 trends
        return trend_data
    except tweepy.TweepError as e:
        logging.error(f"Error fetching trends: {e}")
        return []


# Follow a user (could be used for AI agent accounts following users)
def follow_user(api, user_handle):
    """
    Follow a user on Twitter.
    """
    logging.info(f"Following @{user_handle}...")
    try:
        api.create_friendship(screen_name=user_handle)
        logging.info(f"Successfully followed @{user_handle}.")
    except tweepy.TweepError as e:
        logging.error(f"Error following user: {e}")


# Unfollow a user (useful for unfollowing inactive accounts)
def unfollow_user(api, user_handle):
    """
    Unfollow a user on Twitter.
    """
    logging.info(f"Unfollowing @{user_handle}...")
    try:
        api.destroy_friendship(screen_name=user_handle)
        logging.info(f"Successfully unfollowed @{user_handle}.")
    except tweepy.TweepError as e:
        logging.error(f"Error unfollowing user: {e}")


# Get follower count for a user
def get_follower_count(api, user_handle):
    """
    Get the follower count for a user.
    """
    logging.info(f"Fetching follower count for @{user_handle}...")
    try:
        user = api.get_user(screen_name=user_handle)
        follower_count = user.followers_count
        logging.info(f"@{user_handle} has {follower_count} followers.")
        return follower_count
    except tweepy.TweepError as e:
        logging.error(f"Error fetching follower count: {e}")
        return 0


# Clean tweet text by removing URLs, mentions, and special characters
def clean_tweet_text(tweet_text):
    """
    Clean the tweet text to remove URLs, mentions, and other special characters.
    """
    logging.info("Cleaning tweet text...")
    cleaned_text = re.sub(r'http\S+|www\S+|https\S+', '', tweet_text)  # Remove URLs
    cleaned_text = re.sub(r'@\w+', '', cleaned_text)  # Remove mentions
    cleaned_text = re.sub(r'[^A-Za-z0-9\s]+', '', cleaned_text)  # Remove special characters
    cleaned_text = cleaned_text.strip()  # Remove extra whitespace
    return cleaned_text


# Function to retweet a tweet based on its ID
def retweet(api, tweet_id):
    """
    Retweet a tweet based on its ID.
    """
    logging.info(f"Retweeting tweet with ID: {tweet_id}...")
    try:
        api.retweet(tweet_id)
        logging.info("Retweet successful.")
    except tweepy.TweepError as e:
        logging.error(f"Error retweeting: {e}")


# Like a tweet based on its ID
def like_tweet(api, tweet_id):
    """
    Like a tweet based on its ID.
    """
    logging.info(f"Liking tweet with ID: {tweet_id}...")
    try:
        api.create_favorite(tweet_id)
        logging.info("Tweet liked successfully.")
    except tweepy.TweepError as e:
        logging.error(f"Error liking tweet: {e}")


# Post a tweet with media (image, video, etc.)
def post_media_tweet(api, message, media_path):
    """
    Post a tweet with media (image/video).
    """
    logging.info(f"Posting tweet with media: {message}")
    try:
        media = api.media_upload(media_path)
        api.update_status(status=message, media_ids=[media.media_id])
        logging.info("Tweet with media posted successfully.")
    except tweepy.TweepError as e:
        logging.error(f"Error posting tweet with media: {e}")


# Rate limit handler (sleeping between requests if necessary)
def handle_rate_limit(api):
    """
    Handle rate-limiting by sleeping between requests.
    """
    while True:
        if api.rate_limit_status()['remaining_hits'] > 0:
            break
        logging.warning("Rate limit exceeded. Sleeping for 15 minutes.")
        time.sleep(15 * 60)


# Main integration function
def main():
    api = authenticate_twitter()
    if api is None:
        logging.error("API authentication failed. Exiting.")
        return
    
    # Example use cases
    user_handle = "example_user"
    tweets = fetch_user_timeline(api, user_handle, count=10)
    tweet_data = extract_tweet_data(tweets)
    
    # Analyze sentiment
    sentiment_count = analyze_tweets_sentiment(tweet_data)
    
    # Post a new tweet
    post_tweet(api, "This is a sample tweet from Impetus AI!")
    
    # Follow a user
    follow_user(api, "some_user")
    
    # Get follower count
    get_follower_count(api, user_handle)

    # Fetch trends for a location
    woeid = 1  # Global WOEID for trends
    fetch_trends(api, woeid)


if __name__ == "__main__":
    main()
