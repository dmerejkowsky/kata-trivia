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


class Player:
    def __init__(self, name):
        self.name = name
        self.place = 0
        self.purse = 0
        self.in_penalty_box = False
        self.is_getting_out_of_penalty_box = False

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name


class Game:
    def __init__(self, log):
        self.log = log

        self.players = []
        self.has_ended = False

        self.current_player = None

        self.questions = {c: make_questions(c) for c in Category}

    def info(self, *args):
        self.log.info(*args)

    def is_playable(self):
        return len(self.players) >= 2

    def add(self, player_name):
        new_index = len(self.players) + 1
        player = Player(name=player_name)
        self.players.append(player)
        self.info(player_name, "was added")
        self.info("They are player number", new_index)
        if not self.current_player:
            self.current_player = player

    @property
    def how_many_players(self):
        return len(self.players)

    def roll(self, roll):
        self.info(self.current_player, "is the current player")
        self.info("They have rolled a %s" % roll)

        if self.current_player.in_penalty_box:
            should_advance = self._handle_roll_from_penalty_box(roll)
            if not should_advance:
                return

        self._handle_roll(roll)

    def _ask_question(self):
        questions = self.questions[self.current_category]
        res = questions.pop(0)
        self.info(res)

    def _handle_roll_from_penalty_box(self, roll):
        if roll % 2 != 0:
            self.current_player.is_getting_out_of_penalty_box = True
            self.info(self.current_player, "is getting out of the penalty box")
            return True
        else:
            self.info(self.current_player, "is not getting out of the penalty box")
            self.current_player.is_getting_out_of_penalty_box = False
            return False

    def _handle_roll(self, roll):
        self.advance_current_place(roll)
        self.info(
            f"{self.current_player}'s new location is {self.current_player.place}"
        )
        self.info("The category is", self.current_category.value)
        self._ask_question()

    @property
    def current_category(self):
        return Category.for_place(self.current_player.place)

    def send_current_player_to_penalty_box(self):
        self.current_player.in_penalty_box = True

    def advance_current_place(self, roll):
        current_place = self.current_player.place
        new_place = (current_place + roll) % BOARD_SIZE
        self.current_player.place = new_place

    def next_player(self):
        index = self.players.index(self.current_player)
        next_index = (index + 1) % self.how_many_players
        self.current_player = self.players[next_index]

    def correct_answer(self):
        if (
            self.current_player.in_penalty_box
            and not self.current_player.is_getting_out_of_penalty_box
        ):
            self.next_player()
            return

        self._add_coin()
        self.has_ended = self._did_player_win()
        self.next_player()

    def _add_coin(self):
        self.info("Answer was correct!!!!")
        self.current_player.purse += 1
        self.info(
            self.current_player,
            "now has",
            self.current_player.purse,
            "Gold Coins.",
        )

    def wrong_answer(self):
        self.info("Question was incorrectly answered")
        self.info(self.current_player, "was sent to the penalty box")
        self.send_current_player_to_penalty_box()

        self.next_player()

    def _did_player_win(self):
        return self.current_player.purse == MAX_COINS_IN_PURSE


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
