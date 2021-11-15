from pathlib import Path

import pytest
from conftest import FakeRandomSequence

from trivia import RandomSource


def test_using_a_fake_random_as_iterator():
    """Given start, end and a sequence of results,
    make sure that call to random_in_range() returns
    the proper values
    """

    random_source = FakeRandomSequence(start=1, end=6)
    random_source.set_reference([6, 1, 3])

    actual = list(random_source)
    assert actual == [6, 1, 3]


def test_fake_random_checks_that_references_are_in_range():
    random_source = FakeRandomSequence(start=1, end=6)
    with pytest.raises(ValueError):
        random_source.set_reference([6, 7, 3])


def test_fake_random_using_reference():
    path = Path("reference/randomSeq.txt")
    lines = path.read_text().splitlines()
    random_source = FakeRandomSequence.from_reference(lines[0:2])
    assert random_source.start == 0
    assert random_source.end == 9
    first_three = [next(random_source) for i in range(0, 3)]
    assert first_three == [6, 9, 2]


def test_random_source():
    # This is actually hard to test properly, so let's
    # be real basic here
    random_source = RandomSource(start=1, end=4)
    actual = next(random_source)
    assert 1 <= actual < 4
