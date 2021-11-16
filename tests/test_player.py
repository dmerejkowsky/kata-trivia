from trivia.player import Player


def test_wins_when_max_coins_in_purse():
    player = Player("Alice")
    player.purse = 6
    assert player.did_win(max_coins=6)


def test_still_playing_when_less_than_six_points_in_purse(game):
    player = Player("Alice")
    player.purse = 5
    assert not player.did_win(max_coins=6)
