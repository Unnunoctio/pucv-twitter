from classes.post import Post
from classes.search import Search
from classes.user import User


class TwitterSpider:
    LOGIN_URL = "https://x.com/i/flow/login"

    def __init__(self, user: User):
        self.user = user

    def login(self):
        pass

    def generate_search_url(self, keyword: str | None, account: str | None) -> str:
        if (keyword is not None) and (account is not None):
            return f"https://x.com/search?q=from%3A{account}%20{keyword}&src=typed_query&f=live"
        elif keyword is not None:
            return f"https://x.com/search?q={keyword}&src=typed_query&f=live"
        else:
            return f"https://x.com/search?q=from%3A{account}&src=typed_query&f=live"

    def get_posts(self, search: Search) -> list[Post]:
        pass