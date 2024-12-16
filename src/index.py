import time

from classes.search import Search
from classes.user import User
from config import (
    EMAIL_ACCOUNT,
    EMAIL_SEND,
    SEARCH_ACCOUNT,
    SEARCH_END,
    SEARCH_KEYWORD,
    SEARCH_START,
    TWITTER_EMAIL,
    TWITTER_PASSWORD,
    TWITTER_USERNAME,
)
from spiders.twitter_spider import TwitterSpider
from utils.email import send_email
from utils.excel import write_excel

try:
    start_time = time.time()

    # TODO: VALIDAR DATOS
    user = User(username=TWITTER_USERNAME, email=TWITTER_EMAIL, password=TWITTER_PASSWORD)
    search = Search(keyword=SEARCH_KEYWORD, account=SEARCH_ACCOUNT, start_date=SEARCH_START, end_date=SEARCH_END)

    # TODO: OBTENER POSTS
    twitter_spider = TwitterSpider(user)
    posts = twitter_spider.get_posts(search)

    # TODO: CREAR EXCEL
    file_name = f"twitter_posts_{search.start_date.date()}_{search.end_date.date()}.xlsx"
    write_excel(file_name, posts)

    # TODO: ENVIAR EMAIL
    email_destinatary = EMAIL_SEND if EMAIL_SEND is not None else EMAIL_ACCOUNT
    send_email(email_destinatary, search, file_name)
except ValueError as e:
    print(e)
    exit(1)
finally:
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Tiempo de ejecución: {elapsed_time:.4f} segundos")
