from aiogram.dispatcher.filters.state import State, StatesGroup


class Notifier(StatesGroup):
    name = State()
    targets = State()
    is_enabled = State()


class NotifierEdit(StatesGroup):
    id = State()
    targets = State()
