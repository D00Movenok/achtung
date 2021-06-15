from aiohttp import web
from common.database import async_session
from common.models import Chat
from common.utils import get_chat_by_id
from senders.senders import mapper
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from routers.decorators import admin_auth

chats_route = web.RouteTableDef()


@chats_route.get('/api/chats')
@admin_auth
async def get_chats(request):
    async with async_session() as session:
        statement = select(Chat).options(selectinload(Chat.notifiers))
        chats = await session.execute(statement)

        return web.json_response([
            await item.as_json() for item in chats.scalars()
        ])


# TODO: validate chat type and params
@chats_route.post('/api/chats')
@admin_auth
async def create_chat(request):
    data = await request.json()

    async with async_session() as session:
        chat = Chat(chat_type=data['type'],
                    params=data['params'])
        session.add(chat)

        try:
            await session.commit()
            return web.json_response({
                'status': 'ok',
                'id': chat.id
            })
        except:
            await session.rollback()
            return web.json_response({
                'status': 'error',
                'error': 'Unknown error'
            })


@chats_route.get(r'/api/chats/{id:\d+}')
@admin_auth
async def get_chat(request):
    chat_id = int(request.match_info['id'])

    async with async_session() as session:
        chat = await get_chat_by_id(session, chat_id)

        if chat:
            return web.json_response(await chat.as_json())
        else:
            return web.json_response({})


# TODO: validate chat type and params
@chats_route.put(r'/api/chats/{id:\d+}')
@admin_auth
async def update_chat(request):
    data = await request.json()
    chat_id = int(request.match_info['id'])

    async with async_session() as session:
        chat = await get_chat_by_id(session, chat_id)
        if not chat:
            return web.json_response({
                'status': 'error',
                'error': 'Chat does not exist'
            })

        chat.chat_type = data.get('type', chat.chat_type)
        chat.params = data.get('params', chat.params)

        try:
            await session.commit()
            return web.json_response({
                'status': 'ok'
            })
        except:
            await session.rollback()
            return web.json_response({
                'status': 'error',
                'error': 'Unknown error'
            })


@chats_route.delete(r'/api/chats/{id:\d+}')
@admin_auth
async def delete_chat(request):
    chat_id = int(request.match_info['id'])

    async with async_session() as session:
        chat = await get_chat_by_id(session, chat_id)
        if not chat:
            return web.json_response({
                'status': 'error',
                'error': 'Chat does not exist'
            })

        chat.notifiers = []
        await session.delete(chat)

        try:
            await session.commit()
            return web.json_response({
                'status': 'ok'
            })
        except:
            await session.rollback()
            return web.json_response({
                'status': 'error',
                'error': 'Unknown error'
            })


@chats_route.get('/api/chats/types')
@admin_auth
def get_chat_types(request):
    return web.json_response([
        {'type': key, 'fields': value.required_fields}
        for key, value in mapper.items()
    ])
