import re
from typing import Optional

import bs4
import requests


def get_redirect(title) -> Optional[str]:
    session = requests.Session()
    url = f"https://wikipedia.org/wiki/{title}"
    req = session.get(url=url)
    if not req.ok:
        return None
    soup = bs4.BeautifulSoup(req.text, features="lxml")
    body_content = soup.find("div", id="bodyContent")
    tag_a = body_content.find('a', {
        "class": "mw-redirect",
        "href": re.compile("^/wiki/*")
    })
    return tag_a.string if tag_a else None
