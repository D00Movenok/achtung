import logging

from aiohttp import web

from common.database import engine
from common.models import Base
from routers.chats import chats_route
from routers.notifiers import notifiers_route
from routers.notify import notify_route


async def init_func(argv):
    logging.basicConfig(level=logging.DEBUG)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    app = web.Application()
    app.add_routes(chats_route)
    app.add_routes(notifiers_route)
    app.add_routes(notify_route)

    return app
