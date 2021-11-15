import subprocess
from pathlib import Path


def test_non_regression():
    process = subprocess.run(
        ["python2", "trivia.py"], check=True, capture_output=True, text=True
    )
    actual = process.stdout
    expected = Path("tests/expected.txt").read_text()
    assert actual == expected
