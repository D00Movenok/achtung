import aiogram
from config import ADMIN_ID
from keyboards import chats_callback, chats_types_callback, edit_chat_callback

from .handlers import (back_to_chat, back_to_main, create_chat,
                       create_chat_name_state, create_chat_params_state,
                       create_chat_type_state, del_chat, edit_chat_name_state,
                       edit_chat_params_state, edit_chat_type_state, edit_name,
                       edit_params, edit_type, goto_page, open_chat)
from .states import Chat, ChatName, ChatTypeParams


def register_chats(dp: aiogram.Dispatcher):
    # main chats menu
    dp.register_callback_query_handler(goto_page, chats_callback.filter(
                                       action='goto'),
                                       chat_id=ADMIN_ID)
    dp.register_callback_query_handler(create_chat, chats_callback.filter(
                                       action='create'),
                                       chat_id=ADMIN_ID)
    dp.register_callback_query_handler(back_to_main, chats_callback.filter(
                                       action='back'),
                                       chat_id=ADMIN_ID)
    dp.register_callback_query_handler(open_chat, chats_callback.filter(
                                       action='open'),
                                       chat_id=ADMIN_ID)
    # edit chats menu
    dp.register_callback_query_handler(edit_name, edit_chat_callback.filter(
                                       action='name'), chat_id=ADMIN_ID)
    dp.register_callback_query_handler(edit_type, edit_chat_callback.filter(
                                       action='type'), chat_id=ADMIN_ID)
    dp.register_callback_query_handler(edit_params, edit_chat_callback.filter(
                                       action='params'), chat_id=ADMIN_ID)
    dp.register_callback_query_handler(del_chat, edit_chat_callback.filter(
                                       action='delete'), chat_id=ADMIN_ID)
    dp.register_callback_query_handler(back_to_chat, edit_chat_callback.filter(
                                       action='back'), chat_id=ADMIN_ID)
    # create chat
    dp.register_callback_query_handler(create_chat_type_state,
                                       chats_types_callback.filter(),
                                       state=Chat.type, chat_id=ADMIN_ID)
    dp.register_message_handler(create_chat_name_state, state=Chat.name,
                                chat_id=ADMIN_ID)
    dp.register_message_handler(create_chat_params_state, state=Chat.params,
                                chat_id=ADMIN_ID)
    # edit chat
    dp.register_message_handler(edit_chat_name_state, state=ChatName.id,
                                chat_id=ADMIN_ID)
    dp.register_callback_query_handler(edit_chat_type_state,
                                       chats_types_callback.filter(),
                                       state=ChatTypeParams.type,
                                       chat_id=ADMIN_ID)
    dp.register_message_handler(edit_chat_params_state,
                                state=ChatTypeParams.params,
                                chat_id=ADMIN_ID)
