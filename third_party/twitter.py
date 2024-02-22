import os
from datetime import datetime, timezone
import logging

import tweepy

logger = logging.getLogger("twitter")

auth = tweepy.OAuthHandler(
    os.environ["TWITTER_API_KEY"], os.environ["TWITTER_API_SECRET"]
)
