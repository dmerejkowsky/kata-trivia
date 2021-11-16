def test_game_of_zero_is_not_playable(game):
    assert not game.is_playable()


def test_game_of_one_is_not_playable(game):
    game.add("Alice")
    assert not game.is_playable()


def test_how_many_players(game):
    game.add("Alice")
    game.add("Bob")
    assert game.how_many_players == 2


def test_stays_in_penalty_box_if_roll_is_even(game):
    game.add("Alice")
    bob = game.add("Bob")
    bob.in_penalty_box = True
    game.roll(2)

    assert bob.place == 0
    assert bob.in_penalty_box


def test_do_not_ask_question_if_inside_the_penalty_box(game):
    alice = game.add("Alice")
    alice.in_penalty_box = True
    game.roll(2)

    assert alice.place == 0


def test_ask_question_if_getting_outside_of_the_penalty_box(game):
    alice = game.add("Alice")
    alice.in_penalty_box = True

    game.roll(3)

    assert alice.place == 3


def test_wraps_next_player(game):
    game.add("Alice")
    game.add("Bob")

    assert game.current_player.name == "Alice"

    game.next_player()
    assert game.current_player.name == "Bob"

    game.next_player()
    assert game.current_player.name == "Alice"


def test_answering_correctly_and_winning_the_game(game):
    game.add("Alice")
    game.current_player.purse = 5

    game.correct_answer()

    assert game.has_ended
