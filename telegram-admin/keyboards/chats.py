from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

chats_callback = CallbackData('chats', 'action', 'page')


def chats_get_keyboard(page: int = 0):
    markup = InlineKeyboardMarkup(row_width=2)

    previous_callback_data = chats_callback.new(action='go_to', page=page-1)
    page_callback_data = chats_callback.new(action='page', page=page)
    next_callback_data = chats_callback.new(action='go_to', page=page+1)
    create_callback_data = chats_callback.new(action='create', page=page)
    back_callback_data = chats_callback.new(action='back', page=page)

    pagination = []
    if page > 0:
        pagination.append(
            InlineKeyboardButton('<', callback_data=previous_callback_data)
        )
    pagination.append(
        InlineKeyboardButton('Page', callback_data=page_callback_data)
    )
    # TODO: add next_cb only if next exists
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
