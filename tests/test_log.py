from tests.conftest import SpyLog


def test_log():
    log = SpyLog()
    log.info("One")
    log.info("Two")

    assert log.messages == ["One", "Two"]
