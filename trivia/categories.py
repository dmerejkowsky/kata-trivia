from enum import Enum


class Category(Enum):
    Pop = "Pop"
    Science = "Science"
    Sports = "Sports"
    Rock = "Rock"

    @classmethod
    def for_place(cls, place):
        reminder = place % 4
        if reminder == 0:
            return Category.Pop
        elif reminder == 1:
            return Category.Science
        elif reminder == 2:
            return Category.Sports
        else:
            return Category.Rock
