# https://docs.python.org/3/library/logging.html
# todo: Запустите скрипт в различных режимах отладки , посмотрите
import logging
DEBUG = False
#DEBUG = True

if __name__ == "__main__":

    logger = logging.getLogger()
    logger.name = "My Application"
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s %(name)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if DEBUG:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    logger.warning("Failed to correctly detect operating system.")
    logger.debug("Starting ...")


