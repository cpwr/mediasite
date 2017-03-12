import os
import time
import logging

import aiohttp_debugtoolbar
import aiohttp_jinja2
import jinja2

from aiohttp import web

from app.config import parse_config
from app.admin.controllers import (
    index as admin_index,
    upload,
    blank_page,
    charts,
    tables,
    forms,
    bootstrap_elements,
    bootstrap_grid,
    index_rtl,
)
from app.controllers import (
    contacts,
    portfolio,
    index,
)

from app.lib.db import configure_db_client

log = logging.getLogger(__name__)

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')

async def init_web_app(loop, config):

    app = setup_main_app(config, loop)

    app['config'] = config

    app['db_client'] = await configure_db_client(loop, config['db'])
    log.info("DB client configured")

    app['start_time'] = time.time()

    setup_admin_app(app, loop)
    return app


async def db_shutdown(app):
    db = app['db_client']
    log.info('Closing DB client')
    await db.close()


def add_static_handlers(app):
    app.router.add_static('/static', './static', name='static')


def add_handlers(app):
    app.router.add_route('GET', '/', index, name='index')
    app.router.add_route('GET', '/contacts', contacts, name='contacts')
    app.router.add_route('GET', '/portfolio', portfolio, name='portfolio')


def setup_main_app(config, loop):
    app = web.Application(loop=loop, debug=config['app']['debug'])
    aiohttp_debugtoolbar.setup(app)
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(TEMPLATE_DIR + '/main'),
    )
    app.on_cleanup.append(db_shutdown)

    add_handlers(app)
    add_static_handlers(app)
    return app


def setup_admin_app(app, loop):
    admin = web.Application(loop=loop)
    aiohttp_debugtoolbar.setup(admin)
    add_static_handlers(admin)
    aiohttp_jinja2.setup(
        admin,
        loader=jinja2.FileSystemLoader(TEMPLATE_DIR + '/admin'),
    )
    add_admin_handlers(admin)
    app.add_subapp('/admin/', admin)


def add_admin_handlers(app):
    app.router.add_route('GET', '/', admin_index, name='index')
    app.router.add_route('GET', '/charts', charts, name='charts')
    app.router.add_route('GET', '/blank_page', blank_page, name='blank_page')
    app.router.add_route('GET', '/tables', tables, name='tables')
    app.router.add_route('GET', '/forms', forms, name='forms')
    app.router.add_route('GET', '/bootstrap_elements', bootstrap_elements, name='bootstrap_elements')
    app.router.add_route('GET', '/bootstrap_grid', bootstrap_grid, name='bootstrap_grid')
    app.router.add_route('GET', '/index_rtl', index_rtl, name='index_rtl')
    app.router.add_route('*', '/upload', upload, name='upload')
