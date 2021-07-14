from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

edit_chat_callback = CallbackData('edit_chat', 'action', 'id')


async def edit_chat_get_keyboard(id: int):
    markup = InlineKeyboardMarkup(row_width=1)

    name_callback_data = edit_chat_callback.new(action='name', id=id)
    type_callback_data = edit_chat_callback.new(action='type', id=id)
    params_callback_data = edit_chat_callback.new(action='params', id=id)
    delete_callback_data = edit_chat_callback.new(action='delete', id=id)
    back_callback_data = edit_chat_callback.new(action='back', id=id)

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
