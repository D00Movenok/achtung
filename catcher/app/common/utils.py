from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from common.models import Chat, Notifier


async def get_chat_by_id(session, chat_id):
    stmt = (select(Chat)
            .where(Chat.id == chat_id)
            .options(selectinload(Chat.notifiers)))
    result = await session.execute(stmt)
    chat = result.scalars().first()
    return chat


async def get_chats_by_id(session, id_list):
    stmt = (select(Chat)
            .where(Chat.id.in_(id_list)))
    result = await session.execute(stmt)
    chats = result.scalars().all()
    return chats


async def get_notifier_by_id(session, id):
    stmt = (select(Notifier)
            .where(Notifier.id == id)
            .options(selectinload(Notifier.targets)))
    result = await session.execute(stmt)
    notifier = result.scalars().first()
    return notifier
