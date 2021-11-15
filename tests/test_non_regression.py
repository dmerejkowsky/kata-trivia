import subprocess
from pathlib import Path


def test_non_regression():
    process = subprocess.run(
        ["python3", "trivia.py", "--testing"],
        check=True,
        capture_output=True,
        text=True,
    )
    actual = process.stdout
    expected = Path("reference/result.txt").read_text()
    assert actual == expected
