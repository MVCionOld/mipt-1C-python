from collections import namedtuple
import re

import bs4
import requests
import time


Text = namedtuple(
    'Text', [
        'href',
        'title',
        'content'
    ]
)
AuthorTexts = namedtuple(
    'AuthorTexts', [
        'author',
        'href',
        'texts'
    ]
)


class BooksMiner:

    URL = "http://www.lib.ru/INPROZ/"
    LIMIT = 5

    def __init__(self):
        self.data = []
        self.storage = {}
        self.session = requests.Session()

    def start(self):
        req = self.session.get(url=BooksMiner.URL)
        if req.ok:
            soup = bs4.BeautifulSoup(req.text, features='lxml')
            for i, author_link in enumerate(soup.find_all('li')):
                if i >= BooksMiner.LIMIT:
                    break
                self.data.append(self.observe_author(author_link))

    def observe_author(self, author_url) -> AuthorTexts:
        tag_a = author_url.find('a')
        href = tag_a.attrs["href"]
        author = tag_a.contents[0].contents[0]
        time.sleep(0.5)
        req = self.session.get(url=f"{BooksMiner.URL}{href}")
        texts = []
        if req.ok:
            soup = bs4.BeautifulSoup(req.text, features='lxml')
            text_links = soup.find_all('a', {'href': re.compile("^\S+.txt$")})
            for i, text_link in enumerate(text_links):
                if i >= BooksMiner.LIMIT:
                    break
                content_href = text_link.attrs["href"]
                content_title = text_link.contents[0].contents[0]
                texts.append(Text(
                    href=content_href,
                    title=content_title,
                    content=self.get_content(f"{href}{content_href}")
                ))
        return AuthorTexts(
            author=author,
            href=href,
            texts=texts
        )

    def get_content(self, content_url: str) -> str:
        if content_url in self.storage:
            return self.storage[content_url]
        time.sleep(0.5)
        req = self.session.get(url=f"{BooksMiner.URL}{content_url}")
        if not req.ok:
            return ""
        soup = bs4.BeautifulSoup(req.text, features='lxml')
        content = []
        for sibling in soup.find('pre').next_siblings:
            if isinstance(sibling, bs4.element.NavigableString):
                content.append(str(sibling))
        content = "".join(content)
        self.storage[content_url] = content
        return content


