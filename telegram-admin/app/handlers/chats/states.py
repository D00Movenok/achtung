from aiogram.dispatcher.filters.state import State, StatesGroup


class Chat(StatesGroup):
    type = State()
    name = State()
    params = State()
    params_text = State()


class ChatName(StatesGroup):
    id = State()


class ChatTypeParams(StatesGroup):
    id = State()
    type = State()
    params = State()
    params_text = State()
