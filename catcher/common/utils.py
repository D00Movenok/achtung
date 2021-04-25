from catcher.common.models import Chat, Notifier
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


async def get_notifier_by_id(session, id):
    stmt = (select(Notifier)
            .where(Notifier.id == id)
            .options(selectinload(Notifier.targets)))
    result = await session.execute(stmt)
    notifier = result.scalars().first()
    return notifier


async def get_chats_by_id(session, id_list):
    stmt = select(Chat).where(Chat.id.in_(id_list))
    result = await session.execute(stmt)
    targets = result.scalars().all()
    return targets
