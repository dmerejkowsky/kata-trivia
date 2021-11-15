from conftest import FakeRandomSource


def test_fake_random():
    """Given start, stop and a sequence of results,
    make sure that call to random_in_range() returns
    the proper values
    """

    random_source = FakeRandomSource(start=1, end=6)
    random_source.set_reference([6, 1, 3])

    actual = [random_source.random_in_range() for _ in range(0, 3)]
    assert actual == [6, 1, 3]
