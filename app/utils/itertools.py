import itertools


def partition(l, size):
    it = iter(l)
    return iter(lambda: tuple(itertools.islice(it, size)), ())