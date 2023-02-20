# Sanguosha main


class Game:
    def __init__(self):
        pass


def a(x, y):
    print(x + y)


def b(x):
    print(x)


f = {'a': a, 'b': b}


def g(n, *arg):
    f[n](*arg)


g('a', 3, 4)
g('b', 2)
