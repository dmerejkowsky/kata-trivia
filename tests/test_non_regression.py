from pathlib import Path

from trivia import Log, run_game


def test_non_regression():
    from tests.conftest import FakeRandomSource

    path = Path("reference/randomSeq.txt")
    lines = path.read_text().splitlines()
    random_source = FakeRandomSource()

    random_source.apply_reference(lines[0:2])
    random_source.apply_reference(lines[3:5])
    log = Log(verbose=False)

    run_game(random_source=random_source, log=log)

    actual = log.messages
    breakpoint()
    expected = Path("reference/result.txt").read_text().splitlines()
    assert actual == expected
