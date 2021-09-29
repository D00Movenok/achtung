from aiogram.dispatcher.filters.state import State, StatesGroup


class NotifierCreateState(StatesGroup):
    name = State()
    targets = State()
    is_enabled = State()


class NotifierEditState(StatesGroup):
    id = State()
    targets = State()
