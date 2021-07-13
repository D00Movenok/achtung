from typing import Set

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.emoji import emojize
from config import PAGE_LIMIT
from utils.requests import get_notifier

notifier_chats_callback = CallbackData('create_notifier', 'action', 'page',
                                       'target')

notifiers_enabled_callback = CallbackData('create_notifier', 'enabled')


async def notifier_chats_get_keyboard(page: int = 0, ids: Set[int] = set()):
    markup = InlineKeyboardMarkup(row_width=2)

    previous_callback_data = notifier_chats_callback.new(action='goto',
                                                         page=page-1,
                                                         target=-1)
    next_callback_data = notifier_chats_callback.new(action='goto',
                                                     page=page+1,
                                                     target=-1)
    create_callback_data = notifier_chats_callback.new(action='create',
                                                       page=page,
                                                       target=-1)

    json_resp = await get_notifier(page)
    is_max = len(json_resp) == PAGE_LIMIT
    for chat in json_resp:
        print(chat)
        open_callback_data = notifier_chats_callback.new(
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
        json_resp_next = await get_notifier(page + 1)
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


async def notifier_enable_get_keyboard():
    markup = InlineKeyboardMarkup(row_width=3)

    enabled_callback_data = notifiers_enabled_callback.new(enabled=True)
    disabled_callback_data = notifiers_enabled_callback.new(enabled=False)
    markup.add(
        InlineKeyboardButton('Enable', callback_data=enabled_callback_data)
    )
    markup.add(
        InlineKeyboardButton('Disable', callback_data=disabled_callback_data)
    )

    return markup
