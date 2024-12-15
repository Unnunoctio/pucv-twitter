import os

from dotenv import load_dotenv

load_dotenv(override=True)

TWITTER_USERNAME = os.getenv("TWITTER_USERNAME")
if TWITTER_USERNAME == "":
    TWITTER_USERNAME = None

TWITTER_EMAIL = os.getenv("TWITTER_EMAIL")
if TWITTER_EMAIL == "":
    TWITTER_EMAIL = None

TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")
if TWITTER_PASSWORD == "":
    TWITTER_PASSWORD = None


SEARCH_KEYWORD = os.getenv("SEARCH_KEYWORD")
if SEARCH_KEYWORD == "":
    SEARCH_KEYWORD = None

SEARCH_ACCOUNT = os.getenv("SEARCH_ACCOUNT")
if SEARCH_ACCOUNT == "":
    SEARCH_ACCOUNT = None

SEARCH_START=os.getenv("SEARCH_START") # "aaaa-mm-dd"
if SEARCH_START == "":
    SEARCH_START = None

SEARCH_END=os.getenv("SEARCH_END") # "aaaa-mm-dd"
if SEARCH_END == "":
    SEARCH_END = None

SEND_EMAIL=os.getenv("SEND_EMAIL")
if SEND_EMAIL == "":
    SEND_EMAIL = None