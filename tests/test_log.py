from trivia import Log


def test_log():
    log = Log()
    log.info("One")
    log.info("Two")

    assert log.messages == ["One", "Two"]
