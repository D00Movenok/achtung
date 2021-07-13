from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

edit_notifier_callback = CallbackData('edit_notifier', 'action', 'id')

edit_notifier_chats_callback = CallbackData('edit_notifier', 'action',
                                            'target')


async def edit_notifier_get_keyboard(id: int):
    markup = InlineKeyboardMarkup(row_width=1)

    name_callback_data = edit_notifier_callback.new(action='name', id=id)
    enabled_callback_data = edit_notifier_callback.new(action='is_enabled',
                                                       id=id)
    chats_callback_data = edit_notifier_callback.new(action='chats', id=id)
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
        InlineKeyboardButton('Back', callback_data=back_callback_data)
    )

    return markup
