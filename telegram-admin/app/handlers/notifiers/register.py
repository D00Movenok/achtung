import aiogram
from config import ADMIN_ID

from .handlers import (create_notifier, create_notifier_chats_state,
                       create_notifier_enabled_state,
                       create_notifier_name_state, delete_notifier, edit_chats,
                       edit_is_enabled, edit_name, edit_notifier_chats_state,
                       edit_notifier_name_state, go_back_to_main,
                       go_back_to_notifiers, goto_page, open_notifier)
from .keyboards import (edit_notifier_callback, is_enabled_callback,
                        notifiers_callback, select_chats_callback)
from .states import NotifierCreateState, NotifierEditState


def register_notifiers(dp: aiogram.Dispatcher):
    # main notifiers menu
    dp.register_callback_query_handler(goto_page, notifiers_callback.filter(
                                       action='goto'), chat_id=ADMIN_ID)
    dp.register_callback_query_handler(create_notifier,
                                       notifiers_callback.filter(
                                        action='create'), chat_id=ADMIN_ID)
    dp.register_callback_query_handler(go_back_to_main,
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
    dp.register_callback_query_handler(delete_notifier,
                                       edit_notifier_callback.filter(
                                        action='delete'), chat_id=ADMIN_ID)
    dp.register_callback_query_handler(edit_chats,
                                       edit_notifier_callback.filter(
                                        action='chats'), chat_id=ADMIN_ID)
    dp.register_callback_query_handler(go_back_to_notifiers,
                                       edit_notifier_callback.filter(
                                        action='back'), chat_id=ADMIN_ID)
    # create notifier
    dp.register_message_handler(create_notifier_name_state,
                                state=NotifierCreateState.name,
                                chat_id=ADMIN_ID)
    dp.register_callback_query_handler(create_notifier_chats_state,
                                       select_chats_callback.filter(),
                                       state=NotifierCreateState.targets,
                                       chat_id=ADMIN_ID)
    dp.register_callback_query_handler(create_notifier_enabled_state,
                                       is_enabled_callback.filter(),
                                       state=NotifierCreateState.is_enabled,
                                       chat_id=ADMIN_ID)
    # edit notifier
    dp.register_message_handler(edit_notifier_name_state,
                                state=NotifierEditState.id,
                                chat_id=ADMIN_ID)
    dp.register_callback_query_handler(edit_notifier_chats_state,
                                       select_chats_callback.filter(),
                                       state=NotifierEditState.targets,
                                       chat_id=ADMIN_ID)
