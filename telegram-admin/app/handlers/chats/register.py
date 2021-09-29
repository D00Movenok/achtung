import aiogram
from config import ADMIN_ID

from .handlers import (create_chat, create_chat_name_state,
                       create_chat_params_state, create_chat_type_state,
                       delete_chat, edit_chat_name_state,
                       edit_chat_params_state, edit_chat_type_state, edit_name,
                       edit_params, edit_type, go_back_to_chat,
                       go_back_to_main, goto_page, open_chat)
from .keyboards import chats_callback, edit_callback, types_callback
from .states import ChatCreateState, ChatEditNameState, ChatEditTypeParamsState


def register_chats(dp: aiogram.Dispatcher):
    # main chats menu
    dp.register_callback_query_handler(goto_page, chats_callback.filter(
                                       action='goto'),
                                       chat_id=ADMIN_ID)
    dp.register_callback_query_handler(create_chat, chats_callback.filter(
                                       action='create'),
                                       chat_id=ADMIN_ID)
    dp.register_callback_query_handler(go_back_to_main, chats_callback.filter(
                                       action='back'),
                                       chat_id=ADMIN_ID)
    dp.register_callback_query_handler(open_chat, chats_callback.filter(
                                       action='open'),
                                       chat_id=ADMIN_ID)
    # edit chats menu
    dp.register_callback_query_handler(edit_name, edit_callback.filter(
                                       action='name'), chat_id=ADMIN_ID)
    dp.register_callback_query_handler(edit_type, edit_callback.filter(
                                       action='type'), chat_id=ADMIN_ID)
    dp.register_callback_query_handler(edit_params, edit_callback.filter(
                                       action='params'), chat_id=ADMIN_ID)
    dp.register_callback_query_handler(delete_chat, edit_callback.filter(
                                       action='delete'), chat_id=ADMIN_ID)
    dp.register_callback_query_handler(go_back_to_chat, edit_callback.filter(
                                       action='back'), chat_id=ADMIN_ID)
    # create chat
    dp.register_callback_query_handler(create_chat_type_state,
                                       types_callback.filter(),
                                       state=ChatCreateState.type,
                                       chat_id=ADMIN_ID)
    dp.register_message_handler(create_chat_name_state,
                                state=ChatCreateState.name,
                                chat_id=ADMIN_ID)
    dp.register_message_handler(create_chat_params_state,
                                state=ChatCreateState.params,
                                chat_id=ADMIN_ID)
    # edit chat
    dp.register_message_handler(edit_chat_name_state,
                                state=ChatEditNameState.id,
                                chat_id=ADMIN_ID)
    dp.register_callback_query_handler(edit_chat_type_state,
                                       types_callback.filter(),
                                       state=ChatEditTypeParamsState.type,
                                       chat_id=ADMIN_ID)
    dp.register_message_handler(edit_chat_params_state,
                                state=ChatEditTypeParamsState.params,
                                chat_id=ADMIN_ID)
