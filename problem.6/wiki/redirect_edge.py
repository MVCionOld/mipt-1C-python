from collections import namedtuple


RedirectEdge = namedtuple(
    'RedirectEdge', [
        'from_vertex',
        'to_vertex',
        'type',
        'depth'
    ]
)
