import re
from datetime import timedelta

from playwright.sync_api import ElementHandle, Page, sync_playwright

from classes.post import Post
from classes.search import Search
from classes.user import User


class TwitterSpider:
    X_COM_URL = "https://x.com"
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
        text = article.query_selector("div[data-testid=tweetText]").text_content()

        # TODO: Wrapper Block
        wrapper_div = article.query_selector("div[data-testid='card.wrapper']")
        links = list[str]()
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

    def get_posts(self, search: Search) -> list[Post]:
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=False)
                page = browser.new_page()

                self.login(page)
                page.wait_for_timeout(5000)

                page.goto(self.generate_search_url(search))
                page.wait_for_timeout(3000)
                
                url_posts = set()
                all_posts = list[Post]()
                flag = True
                retry_count = 5
                scroll_position = 0
                scroll_step = 3000


                while flag and retry_count > 0:
                    # TODO: Detectar si paro de obtener información
                    retry_button = page.locator("button:has-text('Retry')")
                    if retry_button.is_visible():
                        print("Retry button visible")
                        page.wait_for_timeout(10*60000) # 10 minutos
                        retry_button.click()
                        retry_count -= 1
                        page.wait_for_timeout(2000)
                        continue
                    
                    # TODO: Obtener los posts
                    retry_count = 5
                    articles = page.query_selector_all("article[data-testid=tweet]")
                    for article in articles:
                        new_post = self.get_post_by_article(article)
                        if new_post.url in url_posts:
                            continue

                        if new_post.date < search.start_date:
                            flag = False
                            break
                        elif new_post.date <= search.end_date:
                            all_posts.append(new_post)
                            url_posts.add(new_post.url)

                    # TODO: Scroll
                    page.evaluate(f"window.scrollBy(0, {scroll_step})")
                    page.wait_for_timeout(2000)

                    new_scroll_position = page.evaluate("window.pageYOffset + window.innerHeight;")
                    if new_scroll_position == scroll_position:
                        flag = False
                        break

                    scroll_position = new_scroll_position

                return all_posts
            except Exception as e:
                raise Exception(e)
            finally:
                browser.close()