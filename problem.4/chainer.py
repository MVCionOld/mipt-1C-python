def chainer(*args):

    result = []

    def _flatten(iterable):
        nonlocal result
    
        def _itermatch(item):
            if hasattr(item, '__iter__') and \
            (len(item) > 1 or not isinstance(item, str)):
                _flatten(item)
            else:
                result.append(item)

        list(map(_itermatch, iterable))
    
    _flatten(args)
    return result


if __name__ == '__main__':
    print(chainer(
        [],
        {-3, -2, -1},
        [1, 2, 3], 
        {"a": 3, "v": 42},  
        {3, 1, 4},
        range(10, 20, 3), 
        "", 
        "why", 
        ["i need", ["do that", ["?"]]]
    ))
