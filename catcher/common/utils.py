from common.models import Chat, Notifier
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


async def get_chat_by_id(session, chat_id):
    statement = (select(Chat)
                 .where(Chat.id == chat_id)
                 .options(selectinload(Chat.notifiers)))

    return (await session.execute(statement)).scalars().first()


async def get_chats_by_id(session, id_list):
    stmt = select(Chat).where(Chat.id.in_(id_list))
    result = await session.execute(stmt)
    targets = result.scalars().all()
    return targets


async def get_notifier_by_id(session, id):
    stmt = (select(Notifier)
            .where(Notifier.id == id)
            .options(selectinload(Notifier.targets)))
    result = await session.execute(stmt)
    notifier = result.scalars().first()
    return notifier
