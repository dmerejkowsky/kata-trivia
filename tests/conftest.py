import pytest

from trivia import Game, RandomSource


class FakeRandomSource:
    def __init__(self):
        self._sequences = {}

    def set_reference(self, range, numbers):
        (start, end) = range
        sequence = FakeRandomSequence(start=start, end=end)
        sequence.set_reference(numbers)
        self._sequences[range] = sequence

    def apply_reference(self, lines):
        sequence = FakeRandomSequence.from_reference(lines)
        self._sequences[(sequence.start, sequence.end)] = sequence

    def in_range(self, start, end):
        sequence = self._sequences[(start, end)]
        return next(sequence)


class FakeRandomSequence:
    def __init__(self, *, start, end):
        self.start = start
        self.end = end
        self._reference = []
        self._index = 0

    @classmethod
    def from_reference(cls, lines):
        header = lines[0]
        start, end = header.split("-")
        res = cls(start=int(start), end=int(end))
        values = lines[1][:-1].split(",")  # strip last ','
        res.set_reference([int(x) for x in values if x])
        return res

    def set_reference(self, numbers):
        for i, number in enumerate(numbers):
            if number < self.start or number > self.end:
                raise ValueError(
                    f"Value {number} at index {i} is not in expected range"
                )

        self._reference = numbers

    def __iter__(self):
        return self

    def __next__(self):
        try:
            res = self._reference[self._index]
        except IndexError:
            raise StopIteration
        self._index += 1
        return res


class SpyLog:
    def __init__(self):
        self.messages = []

    def info(self, *args):
        message = " ".join(str(x) for x in args)
        self.messages.append(message)


@pytest.fixture
def game():
    log = SpyLog()
    return Game(log=log)


@pytest.fixture
def playable_game():
    log = SpyLog()
    game = Game(log=log)
    game.add("Alice")
    game.add("Bob")
    game.add("Charlie")
    return game
