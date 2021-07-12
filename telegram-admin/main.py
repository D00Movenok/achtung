import typing

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiohttp import ClientSession

from config import ADMIN_PASS, API_TOKEN, CATCHER_URL
from keyboards import (chats_callback, chats_get_keyboard,
                       chats_types_callback, chats_types_get_keyboard,
                       main_callback, main_get_keyboard, notifiers_callback,
                       notifiers_get_keyboard)

# TODO: add webhooks
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Chat(StatesGroup):
    type = State()
    name = State()
    params = State()
    params_text = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Select what to do',
                           reply_markup=await main_get_keyboard())


# Main menu keyboard
@dp.callback_query_handler(main_callback.filter(menu=['chats', 'notifiers']))
async def main(query: types.CallbackQuery,
               callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id

    if callback_data['menu'] == 'chats':
        markup = await chats_get_keyboard()
        await bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=markup)
    elif callback_data['menu'] == 'notifiers':
        markup = await notifiers_get_keyboard()
        await bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=markup)
    else:
        await bot.send_message(query.from_user.id,
                               f'{query.data}')


# Chats menu keyboard
@dp.callback_query_handler(chats_callback.filter(
                            action=['goto', 'page', 'create', 'back']))
async def chats(query: types.CallbackQuery,
                callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id

    if callback_data['action'] == 'goto':
        page = int(callback_data['page'])
        markup = await chats_get_keyboard(page)
        await bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=markup)
    elif callback_data['action'] == 'page':
        pass
    elif callback_data['action'] == 'create':
        await Chat.type.set()
        markup = await chats_types_get_keyboard()
        await bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=markup)
    elif callback_data['action'] == 'back':
        markup = await main_get_keyboard()
        await bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=markup)
    else:
        await bot.send_message(query.from_user.id,
                               f'{query.data}')


# Notifiers menu keyboard
@dp.callback_query_handler(notifiers_callback.filter(
                            action=['goto', 'page', 'create', 'back']))
async def notifiers(query: types.CallbackQuery,
                    callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id

    if callback_data['action'] == 'goto':
        page = int(callback_data['page'])
        markup = await notifiers_get_keyboard(page)
        await bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=markup)
    elif callback_data['action'] == 'page':
        pass
    elif callback_data['action'] == 'create':
        pass
    elif callback_data['action'] == 'back':
        markup = await main_get_keyboard()
        await bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=markup)
    else:
        await bot.send_message(query.from_user.id,
                               f'{query.data}')


# Creating chat: select type
@dp.callback_query_handler(chats_types_callback.filter(), state=Chat.type)
async def create_chat_type(message: types.Message, state: FSMContext,
                           callback_data: typing.Dict[str, str]):
    async with state.proxy() as data:
        data['type'] = callback_data['type']

    await Chat.next()
    await bot.send_message(message.from_user.id, 'Enter new chat name:')


# Creating chat: enter name
@dp.message_handler(state=Chat.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        async with ClientSession() as session:
            async with session.get(
                CATCHER_URL + '/api/chats/types',
                headers={'X-Admin-Auth': ADMIN_PASS}
            ) as resp:
                for chat_type in await resp.json():
                    if chat_type['type'] == data['type']:
                        answer = list(chat_type['fields'].values())[0]
                        data['params_text'] = chat_type['fields']
                        data['params'] = dict()

    await Chat.next()
    await bot.send_message(message.from_user.id, f'Enter {answer}:')


# Creating chat: enter params
@dp.message_handler(state=Chat.params)
async def process_params(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        key = list(data['params_text'].keys())[len(data['params'])]
        data['params'][key] = message.text
        if len(data['params']) >= len(data['params_text'].keys()):
            async with ClientSession() as session:
                async with session.post(CATCHER_URL + '/api/chats', headers={
                    'X-Admin-Auth': ADMIN_PASS
                }, json={
                    'type': data['type'],
                    'name': data['name'],
                    'params': data['params']
                }) as resp:
                    json_resp = await resp.json()
                    await state.finish()
                    if json_resp['status'] == 'ok':
                        markup = await chats_get_keyboard()
                        await bot.send_message(message.from_user.id,
                                               'Select what to do',
                                               reply_markup=markup)
                    else:
                        err = json_resp['error']
                        await bot.send_message(message.from_user.id,
                                               f'Something went wrong: {err}')
        else:
            answer = list(data['params_text'].values())[len(data['params'])]
            await bot.send_message(message.from_user.id, f'Enter {answer}:')


if __name__ == '__main__':
    executor.start_polling(dp)
