from uuid import uuid4

from sqlalchemy import (JSON, Boolean, Column, ForeignKey, Integer, String,
                        Table)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

chat_notifier_links = Table(
    'chat_notifier_links', Base.metadata,
    Column('notifier_id', Integer, ForeignKey('notifiers.id')),
    Column('chat_id', Integer, ForeignKey('chats.id'))
)


class Notifiers(Base):
    __tablename__ = 'notifiers'

    id = Column(Integer, primary_key=True)
    access_token = Column(String, nullable=False, unique=True, default=uuid4)
    name = Column(String, nullable=False)
    targets = relationship(
        'Chats',
        secondary=chat_notifier_links,
        back_populates='notifiers'
    )
    is_enabled = Column(Boolean, nullable=False, default=True)


class Chats(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True)
    chat_type = Column('type', String, nullable=False)
    notifiers = relationship(
        'Notifiers',
        secondary=chat_notifier_links,
        back_populates='targets'
    )
    params = Column(JSON, nullable=False)
