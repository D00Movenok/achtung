from aiohttp import web
from catcher.routers.admin_api import admin_route
from catcher.routers.catcher_api import catcher_route
import logging


def init_func(argv):
    logging.basicConfig(level=logging.DEBUG)
    app = web.Application()
    app.add_routes(admin_route)
    app.add_routes(catcher_route)
    return app
