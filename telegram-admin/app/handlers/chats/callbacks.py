from aiogram.utils.callback_data import CallbackData

chats_callback = CallbackData('chats', 'action', 'page')
types_callback = CallbackData('create_chat', 'type')
edit_callback = CallbackData('edit_chat', 'action', 'id')
