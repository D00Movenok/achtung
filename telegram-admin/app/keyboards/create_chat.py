from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from utils.requests import get_types

chats_types_callback = CallbackData('create_chat', 'type')


async def chats_types_get_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)

    types = await get_types()
    for chat_type in types:
        type_callback_data = chats_types_callback.new(
            type=chat_type['type']
        )
        markup.add(
            InlineKeyboardButton(chat_type['type'],
                                 callback_data=type_callback_data)
        )

    return markup
