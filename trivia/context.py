class Log:
    def __init__(self):
        pass

    def info(self, *args):
        print(*args)


log = Log()


def info(*args):
    log.info(*args)
