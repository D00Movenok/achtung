from aiohttp import web
from common.database import async_session
from common.models import Notifier
from common.utils import get_chats_by_id, get_notifier_by_id
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from routers.decorators import admin_auth

notifiers_route = web.RouteTableDef()


@notifiers_route.get('/api/notifiers')
@admin_auth
async def get_notifiers(request):
    offset = int(request.query['offset'])
    limit = int(request.query['limit'])

    async with async_session() as session:
        stmt = select(Notifier).options(selectinload(Notifier.targets))
        if offset is not None and limit is not None:
            stmt = stmt.where(Notifier.id > offset * limit).limit(limit)
        notifiers = await session.execute(stmt)

        return web.json_response([
            await item.as_json() for item in notifiers.scalars()
        ])


@notifiers_route.post('/api/notifiers')
@admin_auth
async def create_notifier(request):
    data = await request.json()

    async with async_session() as session:
        targets_id = set(data['targets'])
        targets = await get_chats_by_id(session, targets_id)
        if len(targets) != len(targets_id):
            return web.json_response({
                'status': 'error',
                'error': 'Not all targets exist'
            })

        notifier = Notifier(
            name=data['name'],
            targets=targets,
            is_enabled=data['is_enabled']
        )
        session.add(notifier)

        try:
            await session.commit()
            return web.json_response({
                'status': 'ok',
                'id': notifier.id,
                'access_token': notifier.access_token
            })
        except:
            await session.rollback()
            return web.json_response({
                'status': 'error',
                'error': 'Unknown error'
            })


@notifiers_route.get('/api/notifiers/{id:\d+}')
@admin_auth
async def get_notifier(request):
    notifier_id = int(request.match_info['id'])

    async with async_session() as session:
        notifier = await get_notifier_by_id(session, notifier_id)

        if notifier:
            return web.json_response(await notifier.as_json())
        else:
            return web.json_response({})


@notifiers_route.put('/api/notifiers/{id:\d+}')
@admin_auth
async def update_notifier(request):
    data = await request.json()
    notifier_id = int(request.match_info['id'])

    async with async_session() as session:
        notifier = await get_notifier_by_id(session, notifier_id)
        if not notifier:
            return web.json_response({
                'status': 'error',
                'error': 'Notifier does not exist'
            })

        if len(data['targets']) > 0:
            targets_id = set(data['targets'])
            targets = await get_chats_by_id(session, targets_id)
            if len(targets) != len(targets_id):
                return web.json_response({
                    'status': 'error',
                    'error': 'Not all targets exist'
                })
            notifier.targets = targets

        notifier.name = data.get('name', notifier.name)
        notifier.is_enabled = data.get('is_enabled', notifier.is_enabled)

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


@notifiers_route.delete('/api/notifiers/{id:\d+}')
@admin_auth
async def delete_notifier(request):
    notifier_id = int(request.match_info['id'])

    async with async_session() as session:
        notifier = await get_notifier_by_id(session, notifier_id)
        if not notifier:
            return web.json_response({
                'status': 'error',
                'error': 'Notifier does not exist'
            })

        notifier.targets = []
        await session.delete(notifier)

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
