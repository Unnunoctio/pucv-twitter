from playwright.sync_api import Browser, sync_playwright

from classes.post import Post
from classes.search import Search
from classes.user import User


class TwitterSpider:
    LOGIN_URL = "https://x.com/i/flow/login"

    def __init__(self, user: User):
        self.user = user

    def login(self, browser: Browser):
        try:
            page = browser.new_page()
            page.goto(self.LOGIN_URL, wait_until="networkidle")

            page.fill('input[name="text"]', self.user.email)
            page.click('text=Next')
            page.wait_for_timeout(1000)

            if page.is_visible('input[name="password"]'):
                page.fill('input[name="password"]', self.user.password)
                page.click('text=Log in')
            else:
                page.fill('input[name="text"]', self.user.username)
                page.click('text=Next')

                page.wait_for_selector('input[name="password"]')
                page.fill('input[name="password"]', self.user.password)
                page.click('text=Log in')

            page.wait_for_timeout(3000)
            return
        except Exception as e:
            browser.close()
            raise Exception(e)

    def generate_search_url(self, keyword: str | None, account: str | None) -> str:
        if (keyword is not None) and (account is not None):
            return f"https://x.com/search?q=from%3A{account}%20{keyword}&src=typed_query&f=live"
        elif keyword is not None:
            return f"https://x.com/search?q={keyword}&src=typed_query&f=live"
        else:
            return f"https://x.com/search?q=from%3A{account}&src=typed_query&f=live"

    def get_posts(self, search: Search) -> list[Post]:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            self.login(browser)

            page = browser.new_page()
            page.goto(self.generate_search_url(search.keyword, search.account), wait_until="networkidle")

            browser.close()

            return []