from conftest import FakeRandomSource
import pytest


def test_using_a_fake_random_as_iterator():
    """Given start, stop and a sequence of results,
    make sure that call to random_in_range() returns
    the proper values
    """

    random_source = FakeRandomSource(start=1, end=6)
    random_source.set_reference([6, 1, 3])

    actual = list(random_source)
    assert actual == [6, 1, 3]


def test_check_that_references_are_in_range():
    random_source = FakeRandomSource(start=1, end=6)
    with pytest.raises(ValueError):
        random_source.set_reference([6, 7, 3])


def test_raises_stop_iteration():
    random_source = FakeRandomSource(start=1, end=6)
    random_source.set_reference([6, 1])

    as_list = list(random_source)
    assert as_list == [6, 1]
