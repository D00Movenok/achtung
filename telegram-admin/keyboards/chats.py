from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from config import PAGE_LIMIT
from utils.requests import get_chats

chats_callback = CallbackData('chats', 'action', 'page')


async def chats_get_keyboard(page: int = 0):
    markup = InlineKeyboardMarkup(row_width=2)

    previous_callback_data = chats_callback.new(action='goto', page=page-1)
    next_callback_data = chats_callback.new(action='goto', page=page+1)
    create_callback_data = chats_callback.new(action='create', page=page)
    back_callback_data = chats_callback.new(action='back', page=page)

    json_resp = await get_chats(page)
    is_max = len(json_resp) == PAGE_LIMIT
    for chat in json_resp:
        open_callback_data = chats_callback.new(action='open',
                                                page=chat['id'])
        markup.add(
            InlineKeyboardButton(chat['name'],
                                 callback_data=open_callback_data)
        )

    if is_max:
        json_resp_next = await get_chats(page + 1)
        is_next = len(json_resp_next) > 0
    else:
        is_next = False

    pagination = []
    if page > 0:
        pagination.append(
            InlineKeyboardButton('<', callback_data=previous_callback_data)
        )
    if is_next:
        pagination.append(
            InlineKeyboardButton('>', callback_data=next_callback_data)
        )

    markup.row(*pagination)
    markup.add(
        InlineKeyboardButton('Create', callback_data=create_callback_data)
    )
    markup.add(
        InlineKeyboardButton('Back', callback_data=back_callback_data)
    )

    return markup
