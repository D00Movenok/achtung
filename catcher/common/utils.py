from common.models import Chat, Notifier
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


async def get_chat_by_id(session, chat_id):
    statement = (select(Chat)
                 .where(Chat.id == chat_id)
                 .options(selectinload(Chat.notifiers)))

    return (await session.execute(statement)).scalars().first()
