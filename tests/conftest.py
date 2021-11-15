class FakeRandomSource:
    def __init__(self, *, start, end):
        self.start = start
        self.end = end
        self._reference = []
        self._index = 0

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
