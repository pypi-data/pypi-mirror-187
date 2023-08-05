from liblog import get_logger

logger = get_logger(top_level=True)


def unmute():
    logger.propagate = True


def mute():
    logger.propagate = False
