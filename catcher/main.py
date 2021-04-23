import logging

from aiohttp import web

from catcher.common.database import engine
from catcher.common.models import Base
from catcher.routers.admin_api import admin_route
from catcher.routers.catcher_api import catcher_route


async def init_func(argv):
    logging.basicConfig(level=logging.DEBUG)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    app = web.Application()
    app.add_routes(admin_route)
    app.add_routes(catcher_route)
    return app
