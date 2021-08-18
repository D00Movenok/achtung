from typing import Set

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.emoji import emojize
from config import PAGE_LIMIT
from utils.requests import get_chats, get_notifier

from .callbacks import (edit_notifier_callback, select_chats_callback,
                        notifiers_callback, is_enabled_callback)


async def get_notifiers_keyboard(page: int = 0):
    markup = InlineKeyboardMarkup(row_width=2)

    previous_callback_data = notifiers_callback.new(action='goto', page=page-1)
    next_callback_data = notifiers_callback.new(action='goto', page=page+1)
    create_callback_data = notifiers_callback.new(action='create', page=page)
    back_callback_data = notifiers_callback.new(action='back', page=page)

    json_resp = await get_notifier(page)
    is_max = len(json_resp) == PAGE_LIMIT
    for notifier in json_resp:
        open_callback_data = notifiers_callback.new(
            action='open',
            page=notifier['id']
        )
        markup.add(
            InlineKeyboardButton(notifier['name'],
                                 callback_data=open_callback_data)
        )

    if is_max:
        json_resp_next = await get_notifier(page+1)
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


async def get_select_chats_keyboard(page: int = 0, ids: Set[int] = set()):
    markup = InlineKeyboardMarkup(row_width=2)

    previous_callback_data = select_chats_callback.new(action='goto',
                                                       page=page-1,
                                                       target=-1)
    next_callback_data = select_chats_callback.new(action='goto',
                                                   page=page+1,
                                                   target=-1)
    create_callback_data = select_chats_callback.new(action='create',
                                                     page=page,
                                                     target=-1)

    json_resp = await get_chats(page)
    is_max = len(json_resp) == PAGE_LIMIT
    for chat in json_resp:
        print(chat)
        open_callback_data = select_chats_callback.new(
            action='add',
            page=page,
            target=chat['id']
        )
        name = chat['name']
        if chat['id'] in ids:
            name += emojize(' :white_check_mark:')
        markup.add(
            InlineKeyboardButton(name,
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
        InlineKeyboardButton('Next', callback_data=create_callback_data)
    )

    return markup


async def get_is_enabled_keyboard():
    markup = InlineKeyboardMarkup(row_width=3)

    enabled_callback_data = is_enabled_callback.new(enabled=True)
    disabled_callback_data = is_enabled_callback.new(enabled=False)
    markup.add(
        InlineKeyboardButton('Enable', callback_data=enabled_callback_data)
    )
    markup.add(
        InlineKeyboardButton('Disable', callback_data=disabled_callback_data)
    )

    return markup


async def get_edit_keyboard(id: int):
    markup = InlineKeyboardMarkup(row_width=1)

    name_callback_data = edit_notifier_callback.new(action='name', id=id)
    enabled_callback_data = edit_notifier_callback.new(action='is_enabled',
                                                       id=id)
    chats_callback_data = edit_notifier_callback.new(action='chats', id=id)
    delete_callback_data = edit_notifier_callback.new(action='delete', id=id)
    back_callback_data = edit_notifier_callback.new(action='back', id=id)

    markup.add(
        InlineKeyboardButton('Edit name', callback_data=name_callback_data)
    )
    markup.add(
        InlineKeyboardButton('Enable/Disable',
                             callback_data=enabled_callback_data)
    )
    markup.add(
        InlineKeyboardButton('Edit chats', callback_data=chats_callback_data)
    )
    markup.add(
        InlineKeyboardButton('Delete', callback_data=delete_callback_data)
    )
    markup.add(
        InlineKeyboardButton('Back', callback_data=back_callback_data)
    )

    return markup
