#!/usr/bin/env python

import random
from enum import Enum

NUM_QUESTIONS_BY_CATEGORY = 50
BOARD_SIZE = 12
MAX_COINS_IN_PURSE = 6


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


def make_questions(category):
    return [
        f"{category.value} Question {i}" for i in range(0, NUM_QUESTIONS_BY_CATEGORY)
    ]


class RandomSource:
    def __init__(self):
        pass

    def in_range(self, start, end):
        return random.randrange(start, end)


class Log:
    def __init__(self):
        pass

    def info(self, *args):
        print(*args)


class Game:
    def __init__(self, log):
        self.log = log

        self.players = []
        self.places = [0] * 6
        self.purses = [0] * 6
        self._in_penalty_box = [0] * 6
        self.has_ended = False

        self._current_player_index = 0
        self.is_getting_out_of_penalty_box = False

        self.questions = {}
        for category in Category:
            self.questions[category] = make_questions(category)

    def info(self, *args):
        self.log.info(*args)

    def is_playable(self):
        return self.how_many_players >= 2

    def add(self, player_name):
        self.players.append(player_name)
        self.places[self.how_many_players] = 0
        self.purses[self.how_many_players] = 0
        self._in_penalty_box[self.how_many_players] = False

        self.info(player_name, "was added")
        self.info("They are player number", len(self.players))

    @property
    def how_many_players(self):
        return len(self.players)

    def roll(self, roll):
        self.info(self.current_player, "is the current player")
        self.info("They have rolled a %s" % roll)

        if self.in_penalty_box:
            should_advance = self._handle_roll_from_penalty_box(roll)
            if not should_advance:
                return

        self._handle_roll(roll)

    def _ask_question(self):
        questions = self.questions[self._current_category]
        res = questions.pop(0)
        self.info(res)

    def _handle_roll_from_penalty_box(self, roll):
        if roll % 2 != 0:
            self.is_getting_out_of_penalty_box = True
            self.info(self.current_player, "is getting out of the penalty box")
            return True
        else:
            self.info(self.current_player, "is not getting out of the penalty box")
            self.is_getting_out_of_penalty_box = False
            return False

    def _handle_roll(self, roll):
        self.advance_current_place(roll)
        self.info(self.current_player + "'s new location is " + str(self.current_place))
        self.info("The category is", self._current_category.value)
        self._ask_question()

    @property
    def _current_category(self):
        return Category.for_place(self.current_place)

    @property
    def current_place(self):
        return self.places[self._current_player_index]

    @property
    def current_player(self):
        return self.players[self._current_player_index]

    @property
    def in_penalty_box(self):
        return self._in_penalty_box[self._current_player_index]

    def advance_current_place(self, roll):
        current_place = self.current_place
        new_place = (current_place + roll) % BOARD_SIZE
        self.places[self._current_player_index] = new_place

    def next_player(self):
        self._current_player_index = (
            self._current_player_index + 1
        ) % self.how_many_players

    def correct_answer(self):
        if self.in_penalty_box and not self.is_getting_out_of_penalty_box:
            self.next_player()
            return

        self._add_coin()
        self.has_ended = self._did_player_win()
        self.next_player()

    def _add_coin(self):
        self.info("Answer was correct!!!!")
        self.purses[self._current_player_index] += 1
        self.info(
            self.current_player,
            "now has",
            self.purses[self._current_player_index],
            "Gold Coins.",
        )

    def wrong_answer(self):
        self.info("Question was incorrectly answered")
        self.info(self.current_player, "was sent to the penalty box")
        self._in_penalty_box[self._current_player_index] = True

        self.next_player()

    def _did_player_win(self):
        return self.purses[self._current_player_index] == MAX_COINS_IN_PURSE


def run_game(*, random_source, log):
    game = Game(log)

    game.add("Chet")
    game.add("Pat")
    game.add("Sue")

    while True:
        game.roll(random_source.in_range(1, 6))

        if random_source.in_range(0, 9) == 7:
            game.wrong_answer()
        else:
            game.correct_answer()

        if game.has_ended:
            break


def main():
    random_source = RandomSource()
    log = Log()

    run_game(random_source=random_source, log=log)


if __name__ == "__main__":
    main()
