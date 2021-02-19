import click
from loguru import logger

from .. import config
from . import misc


@click.group()
def cli():
    from .. import loader
    from . import log

    log.setup()
    loader.setup()


@cli.command()
@click.option("--skip-updates", is_flag=True, default=False, help="Skip pending updates")
def polling(skip_updates: bool):
    """
    Start application in polling mode
    """

    from src.utils.executor import runner

    runner.skip_updates = skip_updates
    runner.start_polling(reset_webhook=True)
    return 0


@cli.command()
@click.option("--skip-updates", is_flag=True, default=False, help="Skip pending updates")
def webhook(skip_updates: bool):
    """
    Start Webhook
    """
    from src.utils.executor import runner

    runner.skip_updates = skip_updates
    runner.on_shutdown(misc.close_webhook, polling=False, webhook=True)
    runner.start_webhook(config.WEBHOOK_PATH, port=config.BOT_PUBLIC_PORT, host="localhost")
    return 0


@cli.command()
@click.argument("user_id", type=int)
@click.option("--remove", "--rm", is_flag=True, default=False, help="Remove superuser rights")
def add_admin(user_id: int, remove: bool):
    from .executor import runner
    from ..loader import db

    try:
        result = runner.start(db.create_admin_user(user_id, remove))
    except Exception as e:
        logger.exception("Failed to create admin: {e}", e=e)
        result = None

    if not result:
        exit(1)
