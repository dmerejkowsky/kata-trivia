import pytest

from trivia.categories import Category


@pytest.mark.parametrize(
    "place,expected",
    [
        (0, Category.Pop),
        (1, Category.Science),
        (2, Category.Sports),
        (3, Category.Rock),
        (4, Category.Pop),
        (5, Category.Science),
        (6, Category.Sports),
        (7, Category.Rock),
        (8, Category.Pop),
        (9, Category.Science),
        (10, Category.Sports),
        (11, Category.Rock),
    ],
)
def test_category_for_place(place, expected):
    actual = Category.for_place(place)
    assert actual == expected
