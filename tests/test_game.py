from trivia import Category


def test_game_of_zero_is_not_playable(game):
    assert not game.is_playable()


def test_game_of_one_is_not_playable(game):
    game.add("Alice")
    assert not game.is_playable()


def test_how_many_players(game):
    game.add("Alice")
    game.add("Bob")
    assert game.how_many_players == 2


def test_roll(game):
    game.add("Alice")
    game.add("Bob")


def test_wins_when_six_points_in_purse(game):
    game.add("Alice")
    game.purses[0] = 6
    assert game._did_player_win()


def test_still_playin_when_less_than_six_points_in_purse(game):
    game.add("Alice")
    game.purses[0] = 5
    assert not game._did_player_win()


def test_simple_roll(game):
    game.add("Alice")
    game.roll(2)

    assert game.current_place == 2
    assert game._current_category == Category.Sports


def test_stays_in_penalty_box_if_roll_is_even(game):
    game.add("Alice")
    game.in_penalty_box[0] = True
    game.roll(2)

    assert game.current_place == 0
    assert game.in_penalty_box[0]


def test_goes_out_of_the_penalty_box_if_roll_is_off(game):
    game.add("Alice")
    game.in_penalty_box[0] = True
    game.roll(3)

    assert game.current_place == 3
    assert game.is_getting_out_of_penalty_box


def test_wraps_current_position(game):
    game.add("Alice")
    game.advance_current_place(10)
    assert game.current_place == 10

    game.advance_current_place(4)
    assert game.current_place == 2


def test_wraps_next_player(game):
    game.add("Alice")
    game.add("Bob")

    assert game.current_player == "Alice"

    game.next_player()
    assert game.current_player == "Bob"

    game.next_player()
    assert game.current_player == "Alice"
