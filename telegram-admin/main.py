import typing

from aiogram import Bot, Dispatcher, executor, types

from keyboards import (chats_callback, chats_get_keyboard, main_callback,
                       main_get_keyboard, notifiers_callback,
                       notifiers_get_keyboard)

# TODO: add webhooks
API_TOKEN = ''

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id,
                           "Select what to do",
                           reply_markup=main_get_keyboard())


@dp.callback_query_handler(main_callback.filter(menu=['chats', 'notifiers']))
async def main(query: types.CallbackQuery,
               callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id

    if callback_data['menu'] == 'chats':
        markup = chats_get_keyboard()
        await bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=markup)
    elif callback_data['menu'] == 'notifiers':
        markup = notifiers_get_keyboard()
        await bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=markup)
    else:
        await bot.send_message(query.from_user.id,
                               f'{query.data}')


@dp.callback_query_handler(chats_callback.filter(
                            action=['go_to', 'page', 'create', 'back']))
async def chats(query: types.CallbackQuery,
                callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id

    if callback_data['action'] == 'goto':
        pass
    elif callback_data['action'] == 'page':
        pass
    elif callback_data['action'] == 'create':
        pass
    elif callback_data['action'] == 'back':
        markup = main_get_keyboard()
        await bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=markup)
    else:
        await bot.send_message(query.from_user.id,
                               f'{query.data}')


@dp.callback_query_handler(notifiers_callback.filter(
                            action=['go_to', 'page', 'create', 'back']))
async def notifiers(query: types.CallbackQuery,
                    callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id

    if callback_data['action'] == 'goto':
        pass
    elif callback_data['action'] == 'page':
        pass
    elif callback_data['action'] == 'create':
        pass
    elif callback_data['action'] == 'back':
        markup = main_get_keyboard()
        await bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=markup)
    else:
        await bot.send_message(query.from_user.id,
                               f'{query.data}')


if __name__ == '__main__':
    executor.start_polling(dp)
