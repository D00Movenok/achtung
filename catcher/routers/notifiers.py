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
    async with async_session() as session:
        stmt = select(Notifier).options(selectinload(Notifier.targets))
        result = await session.execute(stmt)
        response = [await item.as_json() for item in result.scalars()]
    return web.json_response(response)


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

        try:
            new_notifier = Notifier(
                name=data['name'],
                targets=targets,
                is_enabled=data['is_enabled']
            )
            session.add(new_notifier)
            await session.commit()
        except:
            await session.rollback()
            return web.json_response({
                'status': 'error',
                'error': 'Unknown error'
            })

    return web.json_response({
        'status': 'ok',
        'id': new_notifier.id,
        'access_token': new_notifier.access_token
    })


@notifiers_route.get('/api/notifiers/{id}')
@admin_auth
async def get_notifier(request):
    async with async_session() as session:
        response = await get_notifier_by_id(session, request.match_info['id'])

    if not response:
        return web.json_response({})
    else:
        return web.json_response(await response.as_json())


@notifiers_route.put('/api/notifiers/{id}')
@admin_auth
async def update_notifier(request):
    data = await request.json()
    async with async_session() as session:
        notifier = await get_notifier_by_id(session, request.match_info['id'])
        if not notifier:
            return web.json_response({
                'status': 'error',
                'error': 'Non-existent notifier'
            })

        targets_id = set(data['targets'])
        targets = await get_chats_by_id(session, targets_id)
        if len(targets) != len(targets_id):
            return web.json_response({
                'status': 'error',
                'error': 'Not all targets exist'
            })

        try:
            notifier.name = data['name']
            notifier.targets = targets
            notifier.is_enabled = data['is_enabled']
            await session.commit()
        except:
            await session.rollback()
            return web.json_response({
                'status': 'error',
                'error': 'Unknown error'
            })

    return web.json_response({'status': 'ok'})


@notifiers_route.delete('/api/notifiers/{id}')
@admin_auth
async def delete_notifier(request):
    async with async_session() as session:
        try:
            notifier = await get_notifier_by_id(session,
                                                request.match_info['id'])
            if not notifier:
                return web.json_response({
                    'status': 'error',
                    'error': 'Non-existent notifier'
                })

            notifier.targets = []
            await session.delete(notifier)
            await session.commit()
        except:
            await session.rollback()
            return web.json_response({
                'status': 'error',
                'error': 'Unknown error'
            })
    return web.json_response({'status': 'ok'})
