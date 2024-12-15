from datetime import datetime

class Post:
    username: str
    account: str
    date: datetime
    url: str
    text: str
    links: list[str]
    likes: int
    replies: int
    reposts: int
    views: int

    def __init__(self, username: str, account: str, date: str, url: str, text: str, likes: int, replies: int, reposts: int, views: int):
        self.username = username
        self.account = account
        self.date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        self.url = url
        self.text = text
        self.likes = likes
        self.replies = replies
        self.reposts = reposts
        self.views = views