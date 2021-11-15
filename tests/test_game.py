def test_game_of_zero_is_not_playable(game):
    assert not game.is_playable()


def test_game_of_one_is_not_playable(game):
    game.add("Alice")
    assert not game.is_playable()


def test_how_many_players(playable_game):
    assert playable_game.how_many_players == 3
