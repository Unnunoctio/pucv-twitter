import time

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
    start_time = time.time()

    user = User(username=TWITTER_USERNAME, email=TWITTER_EMAIL, password=TWITTER_PASSWORD)
    print(user)

    search = Search(keyword=SEARCH_KEYWORD, account=SEARCH_ACCOUNT, start_date=SEARCH_START, end_date=SEARCH_END)
    print(search)

    twitter_spider = TwitterSpider(user)
    posts = twitter_spider.get_posts(search)
    print(len(posts))

    # SEND EMAIL WITH POSTS
except ValueError as e:
    print(e)
    exit(1)
finally:
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time de ejecución: {elapsed_time:.4f} segundos")
