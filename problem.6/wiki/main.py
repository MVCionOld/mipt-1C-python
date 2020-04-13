import collections
import re
import time

from wiki.redirect_edge import RedirectEdge
from wiki.redirect_graph import RedirectGraph
from wiki.wikirandomapi import get_titles
from wiki.wikiredirect import get_redirect


def traverse(entry_title: str, limit: int = 1, stop_word: str = "philosophy"):
    queue = collections.deque(list(map(
        lambda title_nm: (0, title_nm),
        get_titles(entry_title, limit)
    )))
    redirect_graph = RedirectGraph()
    while queue:
        step, title = queue.popleft()
        print(f"{step}: {title}")
        redirect_title = get_redirect(title)
        if step == 0 and redirect_title is None:
            queue.append((0, get_titles(entry_title, 1)[0]))
        elif redirect_title is None:
            print(f"[NO REDIRECT]: {title}")
            redirect_graph.append(RedirectEdge(
                from_vertex=title,
                to_vertex=None,
                type='DEAD_END',
                depth=step
            ))
            continue
        elif re.search(stop_word, redirect_title.strip().lower()):
            print(f"[FINISH]: {redirect_title}")
            redirect_graph.register(redirect_title)
            redirect_graph.append(RedirectEdge(
                from_vertex=title,
                to_vertex=redirect_title,
                type='FINISH',
                depth=step+1
            ))
            return step + 1
        elif redirect_title in redirect_graph:
            print(f"[CYCLED]: {redirect_title}")
            redirect_graph.append(RedirectEdge(
                from_vertex=title,
                to_vertex=redirect_title,
                type='CYCLE',
                depth=step+1
            ))
        else:
            if step == 0:
                redirect_graph.register(title)
            redirect_graph.register(redirect_title)
            redirect_graph.append(RedirectEdge(
                from_vertex=title,
                to_vertex=redirect_title,
                type='NORMAL',
                depth=step+1
            ))
            queue.append((step + 1, redirect_title))
        time.sleep(0.1)
    return -1


if __name__ == '__main__':
    traverse("Math", 10)
