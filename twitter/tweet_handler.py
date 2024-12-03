import tweepy
import logging
from textblob import TextBlob
import re
import time
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


# Clean tweet text by removing URLs, mentions, and special characters
def clean_tweet_text(tweet_text):
    """
    Clean the tweet text to remove URLs, mentions, and other special characters.
    """
    cleaned_text = re.sub(r'http\S+|www\S+|https\S+', '', tweet_text)  # Remove URLs
    cleaned_text = re.sub(r'@\w+', '', cleaned_text)  # Remove mentions
    cleaned_text = re.sub(r'[^A-Za-z0-9\s]+', '', cleaned_text)  # Remove special characters
    cleaned_text = cleaned_text.strip()  # Remove extra whitespace
    return cleaned_text


# Analyze sentiment of a tweet
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


# Retweet a tweet based on its ID
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


# Respond to a tweet based on its ID
def reply_to_tweet(api, tweet_id, message):
    """
    Reply to a tweet based on its ID.
    """
    logging.info(f"Replying to tweet with ID: {tweet_id}...")
    try:
        api.update_status(status=message, in_reply_to_status_id=tweet_id)
        logging.info("Reply sent successfully.")
    except tweepy.TweepError as e:
        logging.error(f"Error replying to tweet: {e}")


# Filter tweets based on sentiment and retweet or like them
def filter_and_interact(api, tweets, sentiment_threshold=0.1):
    """
    Filter tweets based on sentiment analysis and interact (like/retweet).
    """
    for tweet in tweets:
        cleaned_text = clean_tweet_text(tweet.full_text)
        sentiment = analyze_sentiment(cleaned_text)
        if sentiment == "positive":
            logging.info(f"Tweet is positive: {tweet.full_text}")
            retweet(api, tweet.id)
            like_tweet(api, tweet.id)
        elif sentiment == "negative" and sentiment_threshold:
            logging.info(f"Tweet is negative: {tweet.full_text}")
            reply_to_tweet(api, tweet.id, "Stay strong! 💪")


# Monitor a hashtag for real-time engagement
def monitor_hashtag(api, hashtag, count=100):
    """
    Monitor a hashtag and interact with tweets containing the hashtag.
    """
    logging.info(f"Monitoring hashtag #{hashtag}...")
    for tweet in tweepy.Cursor(api.search_tweets, q=f"#{hashtag}", lang="en", result_type="recent").items(count):
        logging.info(f"Found tweet: {tweet.full_text}")
        cleaned_text = clean_tweet_text(tweet.full_text)
        sentiment = analyze_sentiment(cleaned_text)
        logging.info(f"Sentiment: {sentiment}")
        if sentiment == "positive":
            retweet(api, tweet.id)
            like_tweet(api, tweet.id)
        elif sentiment == "negative":
            reply_to_tweet(api, tweet.id, "We can turn things around!")


# Get trending topics for a location (WOEID)
def get_trending_topics(api, woeid=1):
    """
    Fetch trending topics for a specific WOEID location (Worldwide default).
    """
    logging.info(f"Fetching trending topics for WOEID {woeid}...")
    try:
        trends = api.trends_place(woeid)
        trending_topics = [trend['name'] for trend in trends[0]['trends']]
        logging.info(f"Trending topics: {trending_topics[:5]}")
        return trending_topics
    except tweepy.TweepError as e:
        logging.error(f"Error fetching trends: {e}")
        return []


# Save recent tweets to a DataFrame
def save_tweets_to_dataframe(tweets):
    """
    Save the recent tweets to a pandas DataFrame.
    """
    tweet_data = []
    for tweet in tweets:
        tweet_info = {
            "tweet_id": tweet.id,
            "created_at": tweet.created_at,
            "text": tweet.full_text,
            "likes": tweet.favorite_count,
            "retweets": tweet.retweet_count,
            "sentiment": analyze_sentiment(tweet.full_text)
        }
        tweet_data.append(tweet_info)
    
    df = pd.DataFrame(tweet_data)
    logging.info("Tweets saved to DataFrame.")
    return df


# Get a user's followers and analyze their engagement
def analyze_user_followers(api, user_handle):
    """
    Get a user's followers and analyze their engagement behavior.
    """
    logging.info(f"Analyzing followers of {user_handle}...")
    followers = api.followers(screen_name=user_handle)
    for follower in followers:
        logging.info(f"Follower: {follower.screen_name}, Following: {follower.following_count}, Followers: {follower.followers_count}")
        if follower.followers_count > 5000:
            logging.info(f"Engaging with high-influence follower: {follower.screen_name}")
            like_tweet(api, follower.id)


# Handle incoming replies to a tweet
def handle_incoming_replies(api, tweet_id):
    """
    Handle incoming replies to a specific tweet.
    """
    logging.info(f"Handling incoming replies for tweet ID: {tweet_id}")
    replies = tweepy.Cursor(api.search_tweets, q=f"to:{tweet_id}", since_id=tweet_id, tweet_mode='extended').items()
    for reply in replies:
        logging.info(f"Reply: {reply.full_text}")
        sentiment = analyze_sentiment(reply.full_text)
        if sentiment == "positive":
            logging.info("Positive reply detected, retweeting.")
            retweet(api, reply.id)
        elif sentiment == "negative":
            logging.info("Negative reply detected, replying back.")
            reply_to_tweet(api, reply.id, "Thank you for sharing your thoughts, we appreciate feedback.")


#
