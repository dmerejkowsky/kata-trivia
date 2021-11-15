class FakeRandomSource:
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
