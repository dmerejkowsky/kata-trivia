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
