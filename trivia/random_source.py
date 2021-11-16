import random


class RandomSource:
    def __init__(self):
        pass

    def in_range(self, start, end):
        return random.randrange(start, end)
