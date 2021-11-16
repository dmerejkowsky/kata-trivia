from pathlib import Path

import pytest
from conftest import FakeRandomSequence, FakeRandomSource

from trivia import RandomSource


def test_fake_random_source():
    random_source = FakeRandomSource()
    random_source.set_reference((1, 6), [6, 1, 3])
    actual = [random_source.in_range(1, 6) for _ in range(0, 3)]
    assert actual == [6, 1, 3]


def test_using_a_fake_random_sequence_as_iterator():
    random_sequence = FakeRandomSequence(start=1, end=6)
    random_sequence.set_reference([6, 1, 3])

    actual = list(random_sequence)
    assert actual == [6, 1, 3]


def test_sequence_checks_that_references_are_in_range():
    random_sequence = FakeRandomSequence(start=1, end=6)
    with pytest.raises(ValueError):
        random_sequence.set_reference([6, 7, 3])


def test_sequence_using_reference():
    path = Path("reference/randomSeq.txt")
    lines = path.read_text().splitlines()
    random_sequence = FakeRandomSequence.from_reference(lines[0:2])
    assert random_sequence.start == 0
    assert random_sequence.end == 9
    first_three = [next(random_sequence) for i in range(0, 3)]
    assert first_three == [6, 9, 2]


def test_real_random_source():
    # This is actually hard to test properly, so let's
    # be real basic here
    random_source = RandomSource()
    actual = random_source.in_range(1, 4)
    assert 1 <= actual < 4
