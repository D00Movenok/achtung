import aiogram
from aiogram.dispatcher.filters import Text
from config import ADMIN_ID

from .callbacks import main_callback
from .handlers import cancel, get_id, goto_chats, goto_notifiers, start


def register_main(dp: aiogram.Dispatcher):
    dp.register_message_handler(start, commands=['start'], chat_id=ADMIN_ID)
    dp.register_message_handler(get_id, commands=['id'])
    dp.register_message_handler(cancel, state='*', commands='cancel',
                                chat_id=ADMIN_ID)
    dp.register_message_handler(cancel, Text(equals='cancel',
                                             ignore_case=True), state='*',
                                chat_id=ADMIN_ID)
    dp.register_callback_query_handler(goto_chats,
                                       main_callback.filter(menu='chats'),
                                       chat_id=ADMIN_ID)
    dp.register_callback_query_handler(goto_notifiers,
                                       main_callback.filter(menu='notifiers'),
                                       chat_id=ADMIN_ID)
