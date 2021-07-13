from typing import Dict

from aiohttp import ClientSession
from config import ADMIN_PASS, CATCHER_URL, PAGE_LIMIT


async def get_types():
    async with ClientSession() as session:
        async with session.get(
            CATCHER_URL + '/api/chats/types',
            headers={'X-Admin-Auth': ADMIN_PASS}
        ) as resp:
            json = await resp.json()

    return json


async def get_chats(offset: int):
    async with ClientSession() as session:
        async with session.get(CATCHER_URL + '/api/chats', params={
            'limit': PAGE_LIMIT,
            'offset': offset
        }, headers={'X-Admin-Auth': ADMIN_PASS}) as resp:
            json = await resp.json()

    return json


async def post_chat(params: Dict):
    async with ClientSession() as session:
        async with session.post(CATCHER_URL + '/api/chats',
                                headers={'X-Admin-Auth': ADMIN_PASS},
                                json=params) as resp:
            json = await resp.json()

    return json


async def get_chat_by_id(id: int):
    async with ClientSession() as session:
        async with session.get(
            CATCHER_URL + f'/api/chats/{id}',
            headers={'X-Admin-Auth': ADMIN_PASS}
        ) as resp:
            json = await resp.json()

    return json


async def put_chat(id: int, params: Dict):
    async with ClientSession() as session:
        async with session.put(
            CATCHER_URL + f'/api/chats/{id}',
            headers={'X-Admin-Auth': ADMIN_PASS},
            json=params
        ) as resp:
            json = await resp.json()

    return json


async def get_notifier(offset: int):
    async with ClientSession() as session:
        async with session.get(CATCHER_URL + '/api/notifiers', params={
            'limit': PAGE_LIMIT,
            'offset': offset
        }, headers={'X-Admin-Auth': ADMIN_PASS}) as resp:
            json = await resp.json()

    return json


async def post_notifier(params: Dict):
    async with ClientSession() as session:
        async with session.post(CATCHER_URL + '/api/notifiers',
                                headers={'X-Admin-Auth': ADMIN_PASS},
                                json=params) as resp:
            json = await resp.json()

    return json


async def get_notifier_by_id(id: int):
    async with ClientSession() as session:
        async with session.get(
            CATCHER_URL + f'/api/notifiers/{id}',
            headers={'X-Admin-Auth': ADMIN_PASS}
        ) as resp:
            json = await resp.json()

    return json


async def put_notifier(id: int, params: Dict):
    async with ClientSession() as session:
        async with session.put(
            CATCHER_URL + f'/api/notifiers/{id}',
            headers={'X-Admin-Auth': ADMIN_PASS},
            json=params
        ) as resp:
            json = await resp.json()

    return json
