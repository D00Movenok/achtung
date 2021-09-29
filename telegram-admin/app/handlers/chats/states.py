from aiogram.dispatcher.filters.state import State, StatesGroup


class ChatCreateState(StatesGroup):
    type = State()
    name = State()
    params = State()
    params_text = State()


class ChatEditNameState(StatesGroup):
    id = State()


class ChatEditTypeParamsState(StatesGroup):
    id = State()
    type = State()
    params = State()
    params_text = State()
