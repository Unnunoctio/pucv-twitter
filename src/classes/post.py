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

    def __init__(self, username: str, account: str, date: str, url: str, text: str, links: list[str], likes: int, replies: int, reposts: int, views: int):
        self.username = username
        self.account = account
        self.date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
        self.url = url
        self.text = text
        self.links = links
        self.likes = likes
        self.replies = replies
        self.reposts = reposts
        self.views = views

    def __str__(self):
        return f"Username: {self.username}\nAccount: {self.account}\nDate: {self.date}\nURL: {self.url}\nText: {self.text}\nLinks: {self.links}\nLikes: {self.likes}\nReplies: {self.replies}\nReposts: {self.reposts}\nViews: {self.views}"