#!/usr/bin/env python

from trivia.categories import Category
from trivia.context import info
from trivia.player import Player
from trivia.random_source import RandomSource

NUM_QUESTIONS_BY_CATEGORY = 50
BOARD_SIZE = 12
MAX_COINS_IN_PURSE = 6


def make_questions(category):
    return [
        f"{category.value} Question {i}" for i in range(0, NUM_QUESTIONS_BY_CATEGORY)
    ]


class Game:
    def __init__(self):
        self.players = []
        self.has_ended = False

        self.current_player = None

        self.questions = {c: make_questions(c) for c in Category}

    def is_playable(self):
        return len(self.players) >= 2

    def add(self, player_name):
        new_index = len(self.players) + 1
        player = Player(name=player_name)
        self.players.append(player)
        info(player_name, "was added")
        info("They are player number", new_index)
        if not self.current_player:
            self.current_player = player

    @property
    def how_many_players(self):
        return len(self.players)

    def roll(self, roll):
        info(self.current_player, "is the current player")
        info("They have rolled a %s" % roll)
        self.current_player.on_roll(roll, board_size=BOARD_SIZE)
        if not self.current_player.in_penalty_box:
            self.ask_question()

    def ask_question(self):
        current_place = self.current_player.place
        category = Category.for_place(current_place)
        info("The category is", category.value)
        questions = self.questions[category]
        res = questions.pop(0)
        info(res)

    def send_current_player_to_penalty_box(self):
        self.current_player.in_penalty_box = True

    def next_player(self):
        index = self.players.index(self.current_player)
        next_index = (index + 1) % self.how_many_players
        self.current_player = self.players[next_index]

    def correct_answer(self):
        if (
            self.current_player.in_penalty_box
            and not self.current_player.is_getting_out_of_penalty_box
        ):
            self.has_ended = False
            return

        self._add_coin()
        self.has_ended = self._did_player_win()

    def _add_coin(self):
        info("Answer was correct!!!!")
        self.current_player.purse += 1
        info(
            self.current_player,
            "now has",
            self.current_player.purse,
            "Gold Coins.",
        )

    def wrong_answer(self):
        info("Question was incorrectly answered")
        info(self.current_player, "was sent to the penalty box")
        self.send_current_player_to_penalty_box()

    def _did_player_win(self):
        # TODO
        return self.current_player.purse == MAX_COINS_IN_PURSE


def run_game(*, random_source):
    game = Game()

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
        else:
            game.next_player()


def main():
    random_source = RandomSource()
    run_game(random_source=random_source)


if __name__ == "__main__":
    main()
