from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .callbacks import main_callback


async def get_main_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)

    chats_callback_data = main_callback.new(menu='chats')
    notifiers_callback_data = main_callback.new(menu='notifiers')

    markup.row(
        InlineKeyboardButton('Chats', callback_data=chats_callback_data),
        InlineKeyboardButton('Notifiers',
                             callback_data=notifiers_callback_data)
    )

    return markup
