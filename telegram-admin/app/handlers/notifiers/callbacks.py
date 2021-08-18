from aiogram.utils.callback_data import CallbackData

notifiers_callback = CallbackData('notifiers', 'action', 'page')
select_chats_callback = CallbackData('create_notifier', 'action', 'page',
                                     'target')

is_enabled_callback = CallbackData('create_notifier', 'enabled')
edit_notifier_callback = CallbackData('edit_notifier', 'action', 'id')

edit_chats_callback = CallbackData('edit_notifier', 'action', 'target')
