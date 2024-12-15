from classes.search import Search
from classes.user import User
from config import (
    SEARCH_ACCOUNT,
    SEARCH_END,
    SEARCH_KEYWORD,
    SEARCH_START,
    TWITTER_EMAIL,
    TWITTER_PASSWORD,
    TWITTER_USERNAME,
)
from spiders.twitter_spider import TwitterSpider

try:
    user = User(username=TWITTER_USERNAME, email=TWITTER_EMAIL, password=TWITTER_PASSWORD)
    print(user)

    search = Search(keyword=SEARCH_KEYWORD, account=SEARCH_ACCOUNT, start_date=SEARCH_START, end_date=SEARCH_END)
    print(search)

    twitter_spider = TwitterSpider(user)
    posts = twitter_spider.get_posts(search)
    print(posts)

    # SEND EMAIL WITH POSTS
except ValueError as e:
    print(e)
    exit(1)

