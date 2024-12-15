from playwright.sync_api import Page, sync_playwright

from classes.post import Post
from classes.search import Search
from classes.user import User


class TwitterSpider:
    LOGIN_URL = "https://x.com/i/flow/login"

    def __init__(self, user: User):
        self.user = user

    def login(self, page: Page):
        try:
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

            return
        except Exception as e:
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
            try:
                browser = p.chromium.launch(headless=False)
                page = browser.new_page()
                self.login(page)

                page.wait_for_timeout(5000)
                page.goto(self.generate_search_url(search.keyword, search.account))

                page.wait_for_timeout(5000)
                page.screenshot(path="screenshot.png")
            except Exception as e:
                raise Exception(e)
            finally:
                browser.close()

            return []