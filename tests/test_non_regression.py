import subprocess
from pathlib import Path

import pytest


def test_non_regression():
    process = subprocess.run(
        ["python3", "trivia.py", "--tests"], check=True, capture_output=True, text=True
    )
    actual = process.stdout
    expected = Path("tests/expected.txt").read_text()
    assert actual == expected
