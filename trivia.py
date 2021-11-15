#!/usr/bin/env python

import random
from enum import Enum

NUM_QUESTIONS_BY_CATEGORY = 50


class Category(Enum):
    Pop = "Pop"
    Sience = "Science"
    Sports = "Sports"
    Rock = "Rock"


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
        self.in_penalty_box = [0] * 6

        self.current_player = 0
        self.is_getting_out_of_penalty_box = False

        self.questions = {}
        for category in Category:
            self.questions[category.value] = make_questions(category)

    def is_playable(self):
        return self.how_many_players >= 2

    def info(self, *args):
        self.log.info(*args)

    def add(self, player_name):
        self.players.append(player_name)
        self.places[self.how_many_players] = 0
        self.purses[self.how_many_players] = 0
        self.in_penalty_box[self.how_many_players] = False

        self.info(player_name, "was added")
        self.info("They are player number", len(self.players))

    @property
    def how_many_players(self):
        return len(self.players)

    def roll(self, roll):
        self.info("%s is the current player" % self.players[self.current_player])
        self.info("They have rolled a %s" % roll)

        if self.in_penalty_box[self.current_player]:
            if roll % 2 != 0:
                self.is_getting_out_of_penalty_box = True

                self.info(
                    "%s is getting out of the penalty box"
                    % self.players[self.current_player]
                )
                self.places[self.current_player] = (
                    self.places[self.current_player] + roll
                )
                if self.places[self.current_player] > 11:
                    self.places[self.current_player] = (
                        self.places[self.current_player] - 12
                    )

                self.info(
                    self.players[self.current_player]
                    + "'s new location is "
                    + str(self.places[self.current_player])
                )
                self.info("The category is %s" % self._current_category)
                self._ask_question()
            else:
                self.info(
                    "%s is not getting out of the penalty box"
                    % self.players[self.current_player]
                )
                self.is_getting_out_of_penalty_box = False
        else:
            self.places[self.current_player] = self.places[self.current_player] + roll
            if self.places[self.current_player] > 11:
                self.places[self.current_player] = self.places[self.current_player] - 12

            self.info(
                self.players[self.current_player]
                + "'s new location is "
                + str(self.places[self.current_player])
            )
            self.info("The category is %s" % self._current_category)
            self._ask_question()

    def _ask_question(self):
        questions = self.questions[self._current_category]
        res = questions.pop(0)
        self.info(res)

    @property
    def _current_category(self):
        if self.places[self.current_player] == 0:
            return "Pop"
        if self.places[self.current_player] == 4:
            return "Pop"
        if self.places[self.current_player] == 8:
            return "Pop"
        if self.places[self.current_player] == 1:
            return "Science"
        if self.places[self.current_player] == 5:
            return "Science"
        if self.places[self.current_player] == 9:
            return "Science"
        if self.places[self.current_player] == 2:
            return "Sports"
        if self.places[self.current_player] == 6:
            return "Sports"
        if self.places[self.current_player] == 10:
            return "Sports"
        return "Rock"

    def was_correctly_answered(self):
        if self.in_penalty_box[self.current_player]:
            if self.is_getting_out_of_penalty_box:
                self.info("Answer was correct!!!!")
                self.purses[self.current_player] += 1
                self.info(
                    self.players[self.current_player]
                    + " now has "
                    + str(self.purses[self.current_player])
                    + " Gold Coins."
                )

                winner = self._did_player_win()
                self.current_player += 1
                if self.current_player == len(self.players):
                    self.current_player = 0

                return winner
            else:
                self.current_player += 1
                if self.current_player == len(self.players):
                    self.current_player = 0
                return True

        else:

            self.info("Answer was correct!!!!")
            self.purses[self.current_player] += 1
            self.info(
                self.players[self.current_player]
                + " now has "
                + str(self.purses[self.current_player])
                + " Gold Coins."
            )

            winner = self._did_player_win()
            self.current_player += 1
            if self.current_player == len(self.players):
                self.current_player = 0

            return winner

    def wrong_answer(self):
        self.info("Question was incorrectly answered")
        self.info(self.players[self.current_player] + " was sent to the penalty box")
        self.in_penalty_box[self.current_player] = True

        self.current_player += 1
        if self.current_player == len(self.players):
            self.current_player = 0
        return True

    def _did_player_win(self):
        return not (self.purses[self.current_player] == 6)


def run_game(*, random_source, log):
    game = Game(log)

    game.add("Chet")
    game.add("Pat")
    game.add("Sue")

    continue_game = False
    while True:
        game.roll(random_source.in_range(1, 6))

        if random_source.in_range(0, 9) == 7:
            continue_game = game.wrong_answer()
        else:
            continue_game = game.was_correctly_answered()

        if not continue_game:
            break


def main():
    random_source = RandomSource()
    log = Log()

    run_game(random_source=random_source, log=log)


if __name__ == "__main__":
    main()
