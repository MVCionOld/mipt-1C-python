#!/usr/bin/python3


def create_dict(texts, dictionary=None, sep=' '):
    dictionary = dictionary or dict()
    for text in texts:
        for entry in text.split(sep):
            if dictionary.get(entry, None) is None:
                dictionary[entry] = len(dictionary)
    return dictionary


if __name__ == '__main__':
    d1 = create_dict(["Чо, как"])
    print(d1)
    d2 = create_dict(["Чо , как", "нормально а ти Чо"], d1)
    print(d2, d1 is d2)
