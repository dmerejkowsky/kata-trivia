from trivia.context import info


class Player:
    def __init__(self, name):
        self.name = name
        self.place = 0
        self.purse = 0
        self.in_penalty_box = False
        self.is_getting_out_of_penalty_box = False

    def on_roll(self, roll, board_size):
        if self.in_penalty_box:
            self._handle_roll_from_penalty_box(roll)

        if self.is_getting_out_of_penalty_box or not self.in_penalty_box:
            self.advance(roll, board_size)

    def _handle_roll_from_penalty_box(self, roll):
        if roll % 2 != 0:
            self.is_getting_out_of_penalty_box = True
            info(self.name, "is getting out of the penalty box")
        else:
            info(self.name, "is not getting out of the penalty box")
            self.is_getting_out_of_penalty_box = False

    def advance(self, roll, board_size):
        current_place = self.place
        new_place = (current_place + roll) % board_size
        self.place = new_place
        info(f"{self.name}'s new location is {self.place}")

    def add_coin(self):
        self.purse += 1
        info(
            self.name,
            "now has",
            self.purse,
            "Gold Coins.",
        )

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name
