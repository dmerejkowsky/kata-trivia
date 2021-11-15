class FakeRandomSource:
    def __init__(self, *, start, end):
        self.start = start
        self.end = end
        self._reference = []
        self._index = 0

    def set_reference(self, numbers):
        self._reference = numbers

    def random_in_range(self):
        res = self._reference[self._index]
        self._index += 1
        return res
