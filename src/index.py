import time

from playwright.sync_api import sync_playwright

from classes.post import Post
from classes.search import Search
from classes.user import User
from config import (
    EMAIL_ACCOUNT,
    EMAIL_SEND,
    SEARCH_ACCOUNT,
    SEARCH_END,
    SEARCH_KEYWORD,
    SEARCH_START,
    TWITTER_EMAIL_TEST1,
    TWITTER_EMAIL_TEST2,
    TWITTER_EMAIL_TEST3,
    TWITTER_PASSWORD_TEST1,
    TWITTER_PASSWORD_TEST2,
    TWITTER_PASSWORD_TEST3,
    TWITTER_USERNAME_TEST1,
    TWITTER_USERNAME_TEST2,
    TWITTER_USERNAME_TEST3,
)
from spiders.twitter_spider import TwitterSpider
from utils.email import send_email
from utils.excel import write_excel, delete_excel

try:
    start_time = time.time()

    # TODO: VALIDAR DATOS
    user1 = User(username=TWITTER_USERNAME_TEST1, email=TWITTER_EMAIL_TEST1, password=TWITTER_PASSWORD_TEST1)
    user2 = User(username=TWITTER_USERNAME_TEST2, email=TWITTER_EMAIL_TEST2, password=TWITTER_PASSWORD_TEST2)
    user3 = User(username=TWITTER_USERNAME_TEST3, email=TWITTER_EMAIL_TEST3, password=TWITTER_PASSWORD_TEST3)

    search = Search(keyword=SEARCH_KEYWORD, account=SEARCH_ACCOUNT, start_date=SEARCH_START, end_date=SEARCH_END)

    # TODO: OBTENER POSTS
    all_posts = list[Post]()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        # Para cambiar de usuario, se crean dos spiders
        spiders = [TwitterSpider(browser, user1), TwitterSpider(browser, user2), TwitterSpider(browser, user3)]

        print("Obteniendo posts...")
        swap = 0
        new_search = Search(keyword=search.keyword, account=search.account, start_date=search.start_date.strftime("%Y-%m-%d"), end_date=search.end_date.strftime("%Y-%m-%d"))

        while True:
            # TODO: EJECUTAR SPIDER
            new_posts, is_end, last_date = spiders[swap].get_posts_for_swap(new_search)

            # TODO: GUARDAR POSTS NO REPETIDOS
            for new_post in new_posts:
                if not any(post.url == new_post.url for post in all_posts):
                    all_posts.append(new_post)
            print(f"Posts obtenidos actualmente: {len(all_posts)}")
            
            # TODO: TERMINAR EJECUCIÓN SI YA TERMINO
            if is_end:
                break

            # TODO: ACTUALIZAR EL SEARCH Y EL SWAP
            new_search = Search(keyword=search.keyword, account=search.account, start_date=search.start_date.strftime("%Y-%m-%d"), end_date=last_date.strftime("%Y-%m-%d"))
            swap = (swap + 1) if swap < (len(spiders) - 1) else 0

            # TODO: SLEEP
            time.sleep(15)
        
        browser.close()

    # TODO: CREAR EXCEL
    file_name = f"twitter_posts_{search.start_date.date()}_{search.end_date.date()}.xlsx"
    write_excel(file_name, all_posts)

    # TODO: ENVIAR EMAIL
    email_destinatary = EMAIL_SEND if EMAIL_SEND is not None else EMAIL_ACCOUNT
    send_email(email_destinatary, search, file_name)
    
    # TODO: ELIMINAR EXCEL
    delete_excel(file_name)
except Exception as e:
    print(e.args[0])
    exit(1)
finally:
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Tiempo de ejecución: {elapsed_time:.4f} segundos")
