from trivia.player import Player


def test_wins_when_max_coins_in_purse():
    player = Player("Alice")
    player.purse = 6
    assert player.did_win(max_coins=6)


def test_still_playing_when_less_than_six_points_in_purse(game):
    player = Player("Alice")
    player.purse = 5
    assert not player.did_win(max_coins=6)


def test_simple_roll():
    player = Player("Alice")
    player.on_roll(2, board_size=10)

    assert player.place == 2


def test_wrapping_roll():
    player = Player("Alice")
    player.on_roll(6, board_size=10)
    assert player.place == 6

    player.on_roll(6, board_size=10)

    assert player.place == 2


def test_answering_correctly_when_out_of_the_penalty_box():
    player = Player("Alice")
    player.on_correct_answer()
    assert player.purse == 1


def test_answering_correctly_when_getting_out_of_the_penalty_box():
    player = Player("Alice")
    player.in_penalty_box = True
    player.is_getting_out_of_penalty_box = True

    player.on_correct_answer()

    assert player.purse == 1


def test_going_inside_the_penalty_box_then_out():
    player = Player("Alice")
    player.on_wrong_answer()
    assert player.in_penalty_box

    player.on_roll(3, board_size=10)  # odd
    assert player.in_penalty_box
    assert player.is_getting_out_of_penalty_box

    player.on_correct_answer()
    assert not player.in_penalty_box


def test_going_inside_the_penalty_box_and_staying_there():
    player = Player("Alice")
    player.on_wrong_answer()
    assert player.in_penalty_box

    player.on_roll(2, board_size=10)  # even
    assert player.in_penalty_box
    assert not player.is_getting_out_of_penalty_box


def test_answering_correctly_and_winning_the_game():
    player = Player("Alice")
    player.purse = 5
    player.on_correct_answer()

    assert player.did_win(max_coins=6)
