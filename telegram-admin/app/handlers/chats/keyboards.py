from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import PAGE_LIMIT
from utils.requests import get_chats, get_types

from .callbacks import chats_callback, types_callback, edit_callback


async def get_chats_keyboard(page: int = 0):
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


async def get_types_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)

    types = await get_types()
    for chat_type in types:
        type_callback_data = types_callback.new(
            type=chat_type['type']
        )
        markup.add(
            InlineKeyboardButton(chat_type['type'],
                                 callback_data=type_callback_data)
        )

    return markup


async def get_edit_keyboard(id: int):
    markup = InlineKeyboardMarkup(row_width=1)

    name_callback_data = edit_callback.new(action='name', id=id)
    type_callback_data = edit_callback.new(action='type', id=id)
    params_callback_data = edit_callback.new(action='params', id=id)
    delete_callback_data = edit_callback.new(action='delete', id=id)
    back_callback_data = edit_callback.new(action='back', id=id)

    markup.add(
        InlineKeyboardButton('Edit name', callback_data=name_callback_data)
    )
    markup.add(
        InlineKeyboardButton('Edit type', callback_data=type_callback_data)
    )
    markup.add(
        InlineKeyboardButton('Edit params', callback_data=params_callback_data)
    )
    markup.add(
        InlineKeyboardButton('Delete', callback_data=delete_callback_data)
    )
    markup.add(
        InlineKeyboardButton('Back', callback_data=back_callback_data)
    )

    return markup
