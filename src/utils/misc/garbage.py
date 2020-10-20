from os import path

from src.loader import dp

def setup():
    from src import filters
    from src import middlewares
    from src.utils import executor

    middlewares.setup(dp)
    filters.setup(dp)
    executor.setup()

    logger.info("Configure handlers...")
    # noinspection PyUnresolvedReferences
    import app.handlers