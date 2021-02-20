from aiohttp import web as aio_web
import click
from loguru import logger


@click.group()
def cli():
    from iternal.utils import log

    # logging setup
    log.setup()


@cli.command()
@click.option("--skip-updates", is_flag=True, default=False, help="Skip pending updates")
def polling(skip_updates: bool):
    """
    Start application in polling mode
    """
    from iternal.bot import loader
    from iternal.bot.utils import runner

    loader.setup()
    runner.skip_updates = skip_updates
    runner.start_polling(reset_webhook=True)


@cli.command()
@click.option("--skip-updates", is_flag=True, default=False, help="Skip pending updates")
def webhook(skip_updates: bool):
    """
    Start Webhook
    """
    from iternal.bot import loader
    from iternal import config
    from iternal.bot.utils import misc, runner

    loader.setup()
    runner.skip_updates = skip_updates
    runner.on_shutdown(misc.close_webhook, polling=False, webhook=True)
    runner.start_webhook(config.WEBHOOK_PATH, port=config.BOT_PUBLIC_PORT, host="localhost")


@cli.command()
def web():
    """
    Start Application
    """
    from iternal.web.app import init_app
    from .utils import get_hostandport

    app = init_app()

    host, port = get_hostandport(app.get('config', None))

    aio_web.run_app(
        app,
        host=host,
        port=port,
        print=logger.info
    )


@cli.command()
@click.argument("user_id", type=int)
@click.option("--remove", "--rm", is_flag=True, default=False, help="Remove superuser rights")
def add_admin(user_id: int, remove: bool):
    from iternal.bot.utils import runner
    from iternal.bot.loader import db

    try:
        result = runner.start(db.create_admin_user(user_id, remove))
    except Exception as e:
        logger.exception("Failed to create admin: {e}", e=e)
        result = None

    if not result:
        exit(1)

@cli.command()
@click.option('--test', '-t', default="web", help="runs tests for some application default ['web']\n")
def run_tests(test: str):
    if test is not None:

