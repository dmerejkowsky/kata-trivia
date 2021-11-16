from pathlib import Path

from trivia import context
from trivia.game import main


def test_use_reference():
    main(use_reference=True)

    actual = context.log.messages
    expected = Path("reference/result.txt").read_text().splitlines()
    assert actual == expected
