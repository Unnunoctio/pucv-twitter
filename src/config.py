import os

from dotenv import load_dotenv

load_dotenv(override=True)

def get_env(key: str) -> str | None:
    env = os.getenv(key)
    return env if env != "" else None

# FILTROS
SEARCH_KEYWORD = get_env("SEARCH_KEYWORD")
SEARCH_ACCOUNT = get_env("SEARCH_ACCOUNT")
SEARCH_START = get_env("SEARCH_START") # "aaaa-mm-dd"
SEARCH_END = get_env("SEARCH_END") # "aaaa-mm-dd"

# GMAIL
EMAIL_ACCOUNT = get_env("EMAIL_ACCOUNT")
EMAIL_APP_KEY = get_env("EMAIL_APP_KEY")
EMAIL_SEND = get_env("EMAIL_SEND")

# CUENTAS
TWITTER_USERNAME_TEST1 = get_env("TWITTER_USERNAME_TEST1")
TWITTER_EMAIL_TEST1 = get_env("TWITTER_EMAIL_TEST1")
TWITTER_PASSWORD_TEST1 = get_env("TWITTER_PASSWORD_TEST1")

TWITTER_USERNAME_TEST2 = get_env("TWITTER_USERNAME_TEST2")
TWITTER_EMAIL_TEST2 = get_env("TWITTER_EMAIL_TEST2")
TWITTER_PASSWORD_TEST2 = get_env("TWITTER_PASSWORD_TEST2")

TWITTER_USERNAME_TEST3 = get_env("TWITTER_USERNAME_TEST3")
TWITTER_EMAIL_TEST3 = get_env("TWITTER_EMAIL_TEST3")
TWITTER_PASSWORD_TEST3 = get_env("TWITTER_PASSWORD_TEST3")


