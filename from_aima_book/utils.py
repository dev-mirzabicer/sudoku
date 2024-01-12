import random


def count(seq):
    return sum(bool(x) for x in seq)


def first(iterable, default=None):
    try:
        return iterable[0]
    except IndexError:
        return default
    except TypeError:
        return next(iterable, default)


identity = lambda x: x

argmin = min
argmax = max


def argmin_random_tie(seq, key=identity):
    return argmin(shuffled(seq), key=key)


def shuffled(iterable):
    items = list(iterable)
    random.shuffle(items)
    return items
