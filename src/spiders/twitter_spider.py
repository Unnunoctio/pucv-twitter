import re
from datetime import datetime, timedelta

import pytz
from playwright.sync_api import Browser, BrowserContext, ElementHandle, Page

from classes.post import Post
from classes.search import Search
from classes.user import User


class TwitterSpider:
    X_COM_URL = "https://x.com"
    LOGIN_URL = "https://x.com/i/flow/login"

    user: User
    context: BrowserContext
    page: Page

    def __init__(self, browser: Browser, user: User):
        self.user = user
        self.context = browser.new_context()
        self.page = self.context.new_page()

        # LOGIN
        self.login()

    def login(self):
        try:
            self.page.goto(self.LOGIN_URL, wait_until="networkidle")

            self.page.fill('input[name="text"]', self.user.email)
            self.page.click('text=Next')
            self.page.wait_for_timeout(1000)

            if self.page.is_visible('text=Sorry, we could not find your account.'):
                raise Exception(f"Error: El Correo: {self.user.email} no tiene una cuenta de Twitter")

            if self.page.is_visible('input[name="password"]'):
                self.page.fill('input[name="password"]', self.user.password)
                self.page.click('text=Log in')
            else:
                self.page.fill('input[name="text"]', self.user.username)
                self.page.click('text=Next')

                self.page.wait_for_timeout(1000)
                if self.page.is_visible('text=Incorrect. Please try again.'):
                    raise Exception(f"Error: El Usuario: {self.user.username}, de el Correo: {self.user.email} es incorrecto")

                self.page.wait_for_selector('input[name="password"]')
                self.page.fill('input[name="password"]', self.user.password)
                self.page.click('text=Log in')

                self.page.wait_for_timeout(1000)
                if self.page.is_visible('text=Wrong password!'):
                    raise Exception(f"Error: La Contraseña: {self.user.password}, de el Correo: {self.user.email} es incorrecta")

        except Exception as e:
            raise Exception(e)

    def generate_search_url(self, search: Search) -> str:
        search_url = "https://x.com/search?q="
        if search.keyword is not None:
            search_url += f"{search.keyword}%20"
        if search.account is not None:
            search_url += f"from%3A{search.account}%20"
        
        start_date = search.start_date - timedelta(days=1)
        end_date = search.end_date + timedelta(days=1)
        search_url += f"since%3A{start_date.date()}%20until%3A{end_date.date()}&src=typed_query&f=live"
        return search_url

    def get_post_by_article(self, article: ElementHandle) -> Post:
        # TODO: User-Name Block
        user_links = article.query_selector("div[data-testid=User-Name]").query_selector_all("a")
        username = user_links[0].text_content()
        account = user_links[1].text_content()
        date = user_links[2].query_selector("time").get_attribute("datetime")
        url = user_links[2].get_attribute("href")
        url_post = self.X_COM_URL + url

        # TODO: Text Block
        # TEXT
        text_div = article.query_selector("div[data-testid=tweetText]")
        text = ""
        if text_div is not None:
            text = text_div.text_content()

        # LINKS
        links = list[str]()
        if text_div is not None:
            text_links = text_div.query_selector_all("a")
            for text_link in text_links:
                new_link = text_link.get_attribute("href")
                if new_link[0] == "/":
                    links.append(self.X_COM_URL + new_link)
                else:
                    links.append(new_link)

        # TODO: Wrapper Block
        wrapper_div = article.query_selector("div[data-testid='card.wrapper']")
        if wrapper_div is not None:
            wrapper_links = wrapper_div.query_selector_all("a")
            for wrapper_link in wrapper_links:
                links.append(wrapper_link.get_attribute("href"))

        # TODO: Likes, Replies, Reposts, Views
        replies_btn = article.query_selector("button[data-testid=reply]")
        replies = 0
        if replies_btn is not None:
            replies_text = replies_btn.get_attribute("aria-label")
            match = re.search(r"^\d+", replies_text)
            replies = int(match.group(0)) if match is not None else 0

        reposts_btn = article.query_selector("button[data-testid=retweet]")
        reposts = 0
        if reposts_btn is not None:
            reposts_text = reposts_btn.get_attribute("aria-label")
            match = re.search(r"^\d+", reposts_text)
            reposts = int(match.group(0)) if match is not None else 0

        likes_btn = article.query_selector("button[data-testid=like]")
        likes = 0
        if likes_btn is not None:
            likes_text = likes_btn.get_attribute("aria-label")
            match = re.search(r"^\d+", likes_text)
            likes = int(match.group(0)) if match is not None else 0
        
        views_a = article.query_selector(f"a[href='{url}/analytics']")
        views = 0
        if views_a is not None:
            views_text = views_a.get_attribute("aria-label")
            match = re.search(r"^\d+", views_text)
            views = int(match.group(0)) if match is not None else 0

        return Post(username=username, account=account, date=date, url=url_post, text=text, links=links, likes=likes, replies=replies, reposts=reposts, views=views)

    def get_posts_for_swap(self, search: Search) -> tuple[list[Post], bool, datetime]:
        self.page.goto(self.generate_search_url(search))
        self.page.wait_for_timeout(5000)

        url_posts = set()
        all_posts = list[Post]()
        scroll_position = 0
        scroll_step = 3000

        while True:
            # TODO: Detectar si paro de obtener información
            retry_button = self.page.locator("button:has-text('Retry')")
            if retry_button.is_visible():
                if len(all_posts) == 0:
                    return all_posts, False, search.end_date
                
                last_date_str = all_posts[-1].date.strftime("%Y-%m-%d")
                last_date = datetime.strptime(last_date_str, "%Y-%m-%d")
                last_date = last_date.replace(tzinfo=pytz.utc)
                if last_date < search.start_date:
                    return all_posts, False, search.start_date
                else:
                    return all_posts, False, last_date
        
            # TODO: Obtener los posts
            articles = self.page.query_selector_all("article[data-testid=tweet]")
            for article in articles:
                new_post = self.get_post_by_article(article)
                if new_post.url in url_posts:
                    continue

                if new_post.date < search.start_date:
                    return all_posts, True, search.start_date
                elif new_post.date <= (search.end_date + timedelta(days=1)):
                    all_posts.append(new_post)
                    url_posts.add(new_post.url)
            
            # TODO: Scroll
            self.page.evaluate(f"window.scrollBy(0, {scroll_step})")
            self.page.wait_for_timeout(2000)

            new_scroll_position = self.page.evaluate("window.pageYOffset + window.innerHeight;")
            if new_scroll_position == scroll_position:
                return all_posts, True, search.start_date

            scroll_position = new_scroll_position