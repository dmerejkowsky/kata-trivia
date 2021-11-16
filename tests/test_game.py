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
    game.current_player.purse = 6
    assert game._did_player_win()


def test_still_playin_when_less_than_six_points_in_purse(game):
    game.add("Alice")
    game.current_player.purse = 5
    assert not game._did_player_win()


def test_simple_roll(game):
    game.add("Alice")
    game.roll(2)

    assert game.current_player.place == 2
    assert game._current_category == Category.Sports


def test_stays_in_penalty_box_if_roll_is_even(game):
    game.add("Alice")
    game.send_current_player_to_penalty_box()
    game.roll(2)

    assert game.current_player.place == 0
    assert game.current_player.in_penalty_box


def test_goes_out_of_the_penalty_box_if_roll_is_off(game):
    game.add("Alice")
    game.send_current_player_to_penalty_box()
    game.roll(3)

    assert game.current_player.place == 3
    assert game.current_player.is_getting_out_of_penalty_box


def test_wraps_current_position(game):
    game.add("Alice")
    game.advance_current_place(10)
    assert game.current_player.place == 10

    game.advance_current_place(4)
    assert game.current_player.place == 2


def test_wraps_next_player(game):
    game.add("Alice")
    game.add("Bob")

    assert game.current_player.name == "Alice"

    game.next_player()
    assert game.current_player.name == "Bob"

    game.next_player()
    assert game.current_player.name == "Alice"


def test_is_sent_to_penalty_box_on_wrong_answer(game):
    game.add("Alice")

    game.wrong_answer()

    assert game.current_player.in_penalty_box


def test_answering_correctly_when_out_of_the_penalty_box(game):
    game.add("Alice")

    game.correct_answer()

    assert game.current_player.purse == 1


def test_answering_correctly_when_getting_out_of_the_penalty_box(game):
    game.add("Alice")
    game.send_current_player_to_penalty_box()
    game.current_player.is_getting_out_of_penalty_box = True
    game.current_player.purse = 3

    game.correct_answer()

    assert game.current_player.purse == 4
    assert not game.has_ended


def test_answering_correctly_and_winning_the_game(game):
    game.add("Alice")
    game.current_player.purse = 5

    game.correct_answer()

    assert game.current_player.purse == 6
    assert game.has_ended
