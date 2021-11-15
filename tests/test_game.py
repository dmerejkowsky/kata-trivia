def test_game_of_one_is_not_playable(game):
    game.add("Alice")
    assert not game.is_playable()
