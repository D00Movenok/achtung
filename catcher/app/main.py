import logging

from aiohttp import web
from aiohttp_swagger3 import SwaggerFile, SwaggerUiSettings

from common.database import engine
from common.models import Base
from routers.chats import chats_route
from routers.notifiers import notifiers_route
from routers.notify import notify_route
from os import getenv

API_DOC_ENABLED = getenv('API_DOC_ENABLED', 'false').lower() == 'true'


async def init_func():
    logging.basicConfig(level=logging.INFO)

    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    app = web.Application()

    if API_DOC_ENABLED:
        router = SwaggerFile(
            app,
            spec_file='specs.yml',
            validate=False,
            swagger_ui_settings=SwaggerUiSettings(path='/api/docs')
        )
    else:
        router = app

    router.add_routes(chats_route)
    router.add_routes(notifiers_route)
    router.add_routes(notify_route)

    return app
