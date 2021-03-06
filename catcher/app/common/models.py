from uuid import uuid4

from sqlalchemy import (JSON, Boolean, Column, ForeignKey, Integer, String,
                        Table)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

chat_notifier_links = Table(
    'chat_notifier_links', Base.metadata,
    Column('notifier_id', Integer, ForeignKey('notifier.id')),
    Column('chat_id', Integer, ForeignKey('chat.id'))
)


class Notifier(Base):
    __tablename__ = 'notifier'

    id = Column(Integer, primary_key=True)
    access_token = Column(String, nullable=False, unique=True,
                          default=lambda: uuid4().hex)
    name = Column(String, nullable=False)
    targets = relationship(
        'Chat',
        secondary=chat_notifier_links,
        back_populates='notifiers'
    )
    is_enabled = Column(Boolean, nullable=False, default=True)

    async def as_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'access_token': self.access_token,
            'targets': [target.id for target in self.targets],
            'is_enabled': self.is_enabled
        }


class Chat(Base):
    __tablename__ = 'chat'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    chat_type = Column('type', String, nullable=False)
    notifiers = relationship(
        'Notifier',
        secondary=chat_notifier_links,
        back_populates='targets'
    )
    params = Column(JSON, nullable=False)

    async def as_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.chat_type,
            'notifiers': [notifier.id for notifier in self.notifiers],
            'params': self.params
        }
