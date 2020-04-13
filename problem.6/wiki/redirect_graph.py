from wiki.redirect_edge import RedirectEdge


class RedirectGraph:

    def __init__(self):
        self.history = set()
        self.redirects = []

    def __contains__(self, item):
        return item in self.history

    def append(self, redirect_edge: RedirectEdge):
        self.redirects.append(redirect_edge)

    def register(self, vertex):
        self.history.add(vertex)
