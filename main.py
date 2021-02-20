import logging
from core.commands import run


LOGGER = logging.getLogger(__name__)


if __name__ == '__main__':
    LOGGER.info('Ready.')
    run()
