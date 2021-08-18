import aiogram
from config import ADMIN_ID
from keyboards import (edit_notifier_callback, notifier_chats_callback,
                       notifiers_callback, notifiers_enabled_callback)

from .handlers import (back_to_main, back_to_notifiers, create_notifier,
                       create_notifier_chats_state,
                       create_notifier_enabled_state,
                       create_notifier_name_state, del_notifier, edit_chats,
                       edit_is_enabled, edit_name, edit_notifier_chats_state,
                       edit_notifier_name_state, goto_page, open_notifier)
from .states import Notifier, NotifierEdit


def register_notifiers(dp: aiogram.Dispatcher):
    # main notifiers menu
    dp.register_callback_query_handler(goto_page, notifiers_callback.filter(
                                       action='goto'), chat_id=ADMIN_ID)
    dp.register_callback_query_handler(create_notifier,
                                       notifiers_callback.filter(
                                        action='create'), chat_id=ADMIN_ID)
    dp.register_callback_query_handler(back_to_main,
                                       notifiers_callback.filter(
                                        action='back'), chat_id=ADMIN_ID)
    dp.register_callback_query_handler(open_notifier,
                                       notifiers_callback.filter(
                                        action='open'), chat_id=ADMIN_ID)
    # edit notifiers menu
    dp.register_callback_query_handler(edit_name,
                                       edit_notifier_callback.filter(
                                        action='name'),
                                       chat_id=ADMIN_ID)
    dp.register_callback_query_handler(edit_is_enabled,
                                       edit_notifier_callback.filter(
                                        action='is_enabled'), chat_id=ADMIN_ID)
    dp.register_callback_query_handler(del_notifier,
                                       edit_notifier_callback.filter(
                                        action='delete'), chat_id=ADMIN_ID)
    dp.register_callback_query_handler(edit_chats,
                                       edit_notifier_callback.filter(
                                        action='chats'), chat_id=ADMIN_ID)
    dp.register_callback_query_handler(back_to_notifiers,
                                       edit_notifier_callback.filter(
                                        action='back'), chat_id=ADMIN_ID)
    # create notifier
    dp.register_message_handler(create_notifier_name_state,
                                state=Notifier.name,
                                chat_id=ADMIN_ID)
    dp.register_callback_query_handler(create_notifier_chats_state,
                                       notifier_chats_callback.filter(),
                                       state=Notifier.targets,
                                       chat_id=ADMIN_ID)
    dp.register_callback_query_handler(create_notifier_enabled_state,
                                       notifiers_enabled_callback.filter(),
                                       state=Notifier.is_enabled,
                                       chat_id=ADMIN_ID)
    # edit notifier
    dp.register_message_handler(edit_notifier_name_state,
                                state=NotifierEdit.id,
                                chat_id=ADMIN_ID)
    dp.register_callback_query_handler(edit_notifier_chats_state,
                                       notifier_chats_callback.filter(),
                                       state=NotifierEdit.targets,
                                       chat_id=ADMIN_ID)
