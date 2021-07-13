from functools import wraps

from aiohttp import web
from config import ADMIN_PASS


def admin_auth(handler):
    @wraps(handler)
    async def inner(request):
        if 'X-Admin-Auth' not in request.headers or \
                request.headers['X-Admin-Auth'] != ADMIN_PASS:

            return web.HTTPUnauthorized()

        return await handler(request)

    return inner
