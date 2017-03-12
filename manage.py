import sys
import logging
import asyncio

import click
import uvloop

from app import init_web_app
from app.config import parse_config

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)


async def create_app(loop, host, port, config):

    config = parse_config(config)

    app = await init_web_app(loop, config)

    handler = app.make_handler()
    srv = await loop.create_server(handler, host, port)
    log.info("Running server on %s:%s" % (host, port))
    return app, srv, handler


@click.command()
@click.option(
    "-o", "--host",
    help="Host",
    default='0.0.0.0',
)
@click.option(
    "-p", "--port",
    help="Port",
    default=8000,
)
@click.option(
    "-c", "--config",
    help="Config",
    default='config/dev.yaml',
)
def runserver(host, port, config):
    loop = asyncio.get_event_loop()
    app, srv, handler = loop.run_until_complete(create_app(loop, host, port, config))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.close()
        loop.run_until_complete(srv.wait_closed())
        loop.run_until_complete(app.shutdown())
        loop.run_until_complete(app.cleanup())
        loop.run_until_complete(handler.shutdown(30))
    loop.close()

if __name__ == '__main__':
    runserver()
