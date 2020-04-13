from operator import itemgetter
from typing import List

import requests


def get_titles(gsrsearch: str, limit: int = 5) -> List[str]:
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'generator': 'search',
        'origin': '*',
        'gsrsearch': {gsrsearch},
        'format': 'json',
        'gsrlimit': f'{limit}'
    }
    session = requests.Session()
    req = session.get(url=url, params=params)
    data = req.json()
    titles_list = list(map(
        itemgetter("title"),
        data["query"]["pages"].values()
    ))
    return titles_list
