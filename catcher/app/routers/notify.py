from aiohttp import web
from common.database import async_session
from common.models import Notifier
from senders.senders import mapper
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

notify_route = web.RouteTableDef()


@notify_route.post('/api/notify')
async def notify(request):
    data = await request.json()

    async with async_session() as session:
        stmt = (select(Notifier)
                .where(Notifier.access_token == data['access_token'])
                .options(selectinload(Notifier.targets)))
        result = await session.execute(stmt)
        notifier = result.scalars().first()
        if notifier.is_enabled:
            for chat in notifier.targets:
                sender_class = mapper[chat.chat_type]
                sender = sender_class(**chat.params)
                await sender.send(data['message'])
            return web.StreamResponse(status=200)
        else:
            return web.json_response({
                'status': 'err',
                'error': 'Notifier is disabled'
            })
