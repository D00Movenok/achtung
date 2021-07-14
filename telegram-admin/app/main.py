import logging
import typing

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.executor import Executor
from aiohttp import web

from config import ADMIN_ID, API_TOKEN, LOGS, WEBHOOK_HOST, WEBHOOK_PATH
from keyboards import (chats_callback, chats_get_keyboard,
                       chats_types_callback, chats_types_get_keyboard,
                       edit_chat_callback, edit_chat_get_keyboard,
                       edit_notifier_callback, edit_notifier_get_keyboard,
                       main_callback, main_get_keyboard,
                       notifier_chats_callback, notifier_chats_get_keyboard,
                       notifier_enable_get_keyboard, notifiers_callback,
                       notifiers_enabled_callback, notifiers_get_keyboard)
from utils.requests import (delete_chat, delete_notifier, get_chat_by_id,
                            get_notifier_by_id, get_types, post_chat,
                            post_notifier, put_chat, put_notifier)
from utils.text import chat_info, notifier_info

WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"


bot = Bot(token=API_TOKEN)

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 8080


class Chat(StatesGroup):
    type = State()
    name = State()
    params = State()
    params_text = State()


class ChatName(StatesGroup):
    id = State()


class ChatTypeParams(StatesGroup):
    id = State()
    type = State()
    params = State()
    params_text = State()


class Notifier(StatesGroup):
    name = State()
    targets = State()
    is_enabled = State()


class NotifierEdit(StatesGroup):
    id = State()
    targets = State()


async def start(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Select what to do:',
                           reply_markup=await main_get_keyboard())


async def cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(message.from_user.id,
                           'Cancelled.',
                           reply_markup=types.ReplyKeyboardRemove())


# Main menu keyboard
async def main(query: types.CallbackQuery,
               callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id

    if callback_data['menu'] == 'chats':
        markup = await chats_get_keyboard()
        await bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text='Chats menu:',
                                    reply_markup=markup)
    elif callback_data['menu'] == 'notifiers':
        markup = await notifiers_get_keyboard()
        await bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text='Notifiers menu:',
                                    reply_markup=markup)


# Chats menu keyboard
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
    elif callback_data['action'] == 'open':
        id = callback_data['page']
        chat_data = await get_chat_by_id(id)
        text = await chat_info(chat_data)
        markup = await edit_chat_get_keyboard(id)
        await bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=text,
                                    reply_markup=markup)
    elif callback_data['action'] == 'create':
        await Chat.type.set()
        markup = await chats_types_get_keyboard()
        await bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text='Select chat type:',
                                    reply_markup=markup)
    elif callback_data['action'] == 'back':
        markup = await main_get_keyboard()
        await bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text='Select what to do:',
                                    reply_markup=markup)


# Edit chat menu keyboard
async def edit_chat(query: types.CallbackQuery,
                    callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id

    if callback_data['action'] == 'name':
        await ChatName.id.set()
        state = Dispatcher.get_current().current_state()
        await state.update_data(id=int(callback_data['id']))
        await bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text='Enter new chat name:')
    elif callback_data['action'] == 'type':
        await ChatTypeParams.type.set()
        chat_data = await get_chat_by_id(int(callback_data['id']))
        state = Dispatcher.get_current().current_state()
        await state.update_data(id=int(callback_data['id']))
        await state.update_data(type=chat_data['type'])
        markup = await chats_types_get_keyboard()
        await bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text='Enter new chat name:',
                                    reply_markup=markup)
    elif callback_data['action'] == 'params':
        await ChatTypeParams.params.set()
        chat_data = await get_chat_by_id(int(callback_data['id']))
        state = Dispatcher.get_current().current_state()
        async with state.proxy() as data:
            data['id'] = int(callback_data['id'])
            data['type'] = chat_data['type']
            types = await get_types()
            for chat_type in types:
                if chat_type['type'] == chat_data['type']:
                    answer = list(chat_type['fields'].values())[0]
                    data['params_text'] = chat_type['fields']
                    data['params'] = dict()

        await bot.send_message(chat_id, f'Enter {answer}:')
    elif callback_data['action'] == 'delete':
        json_resp = await delete_chat(int(callback_data['id']))
        if json_resp['status'] == 'ok':
            markup = await chats_get_keyboard()
            await bot.edit_message_text(chat_id=chat_id,
                                        message_id=message_id,
                                        text='Chats menu:',
                                        reply_markup=markup)
        else:
            err = json_resp['error']
            await bot.edit_message_text(chat_id=chat_id,
                                        message_id=message_id,
                                        text=f'Something went wrong: {err}')
    elif callback_data['action'] == 'back':
        markup = await chats_get_keyboard()
        await bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text='Chats menu:',
                                    reply_markup=markup)


# Notifiers menu keyboard
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
    elif callback_data['action'] == 'open':
        id = callback_data['page']
        notifier_data = await get_notifier_by_id(id)
        text = await notifier_info(notifier_data)
        markup = await edit_notifier_get_keyboard(id)
        await bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=text,
                                    reply_markup=markup)
    elif callback_data['action'] == 'create':
        await Notifier.name.set()
        await bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text='Enter new notifier name:')
    elif callback_data['action'] == 'back':
        markup = await main_get_keyboard()
        await bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text='Select what to do:',
                                    reply_markup=markup)


# Edit notifier menu keyboard
async def edit_notifier(query: types.CallbackQuery,
                        callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id

    if callback_data['action'] == 'name':
        await NotifierEdit.id.set()
        state = Dispatcher.get_current().current_state()
        await state.update_data(id=int(callback_data['id']))
        await bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text='Enter new notifier name:')
    elif callback_data['action'] == 'is_enabled':
        id = int(callback_data['id'])
        json_resp = await get_notifier_by_id(id)
        params = {'is_enabled': not json_resp['is_enabled']}
        json_resp_put = await put_notifier(id, params)
        if json_resp_put['status'] == 'ok':
            json_resp_get = await get_notifier_by_id(id)
            text = await notifier_info(json_resp_get)
            markup = await edit_notifier_get_keyboard(id)
            await bot.edit_message_text(chat_id=chat_id,
                                        message_id=message_id,
                                        text=text,
                                        reply_markup=markup)
        else:
            err = json_resp_put['error']
            await bot.send_message(chat_id,
                                   f'Something went wrong: {err}')
    elif callback_data['action'] == 'chats':
        id = int(callback_data['id'])
        json_resp = await get_notifier_by_id(id)
        await NotifierEdit.targets.set()
        state = Dispatcher.get_current().current_state()
        await state.update_data(id=int(callback_data['id']))
        await state.update_data(targets=set(json_resp['targets']))
        markup = await notifier_chats_get_keyboard(0,
                                                   set(json_resp['targets']))
        await bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text='Select chats for notifications:',
                                    reply_markup=markup)
    elif callback_data['action'] == 'delete':
        json_resp = await delete_notifier(int(callback_data['id']))
        if json_resp['status'] == 'ok':
            markup = await notifiers_get_keyboard()
            await bot.edit_message_text(chat_id=chat_id,
                                        message_id=message_id,
                                        text='Notifiers menu:',
                                        reply_markup=markup)
        else:
            err = json_resp['error']
            await bot.edit_message_text(chat_id=chat_id,
                                        message_id=message_id,
                                        text=f'Something went wrong: {err}')
    elif callback_data['action'] == 'back':
        markup = await notifiers_get_keyboard()
        await bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text='Notifiers menu:',
                                    reply_markup=markup)


# Creating chat: select type
async def create_chat_type(query: types.CallbackQuery, state: FSMContext,
                           callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id

    async with state.proxy() as data:
        data['type'] = callback_data['type']

    await Chat.next()
    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text='Enter new chat name:')


# Creating chat: enter name
async def create_chat_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        types = await get_types()
        for chat_type in types:
            if chat_type['type'] == data['type']:
                answer = list(chat_type['fields'].values())[0]
                data['params_text'] = chat_type['fields']
                data['params'] = dict()

    await Chat.next()
    await bot.send_message(message.from_user.id, f'Enter {answer}:')


# Creating chat: enter params
async def create_chat_params(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        key = list(data['params_text'].keys())[len(data['params'])]
        data['params'][key] = message.text
        if len(data['params']) >= len(data['params_text'].keys()):
            params = {
                'type': data['type'],
                'name': data['name'],
                'params': data['params']
            }
            json_resp = await post_chat(params)
            await state.finish()
            if json_resp['status'] == 'ok':
                chat_data = await get_chat_by_id(json_resp['id'])
                text = await chat_info(chat_data)
                markup = await edit_chat_get_keyboard(json_resp['id'])
                await bot.send_message(message.from_user.id,
                                       text,
                                       reply_markup=markup)
            else:
                err = json_resp['error']
                await bot.send_message(message.from_user.id,
                                       f'Something went wrong: {err}')
        else:
            answer = list(data['params_text'].values())[len(data['params'])]
            await bot.send_message(message.from_user.id, f'Enter {answer}:')


# Edit chat: name
async def edit_chat_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        params = {'name': message.text}
        id = data['id']

    ans = await put_chat(id, params)

    await state.finish()
    if ans['status'] == 'ok':
        chat_data = await get_chat_by_id(id)
        text = await chat_info(chat_data)
        markup = await edit_chat_get_keyboard(id)
        await bot.send_message(message.from_user.id,
                               text,
                               reply_markup=markup)
    else:
        err = ans['error']
        await bot.send_message(message.from_user.id,
                               f'Something went wrong: {err}')


# Edit chat: select type
async def edit_chat_type(query: types.CallbackQuery, state: FSMContext,
                         callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id

    async with state.proxy() as data:
        if data['type'] == callback_data['type']:
            id = data['id']
            chat_data = await get_chat_by_id(id)
            text = await chat_info(chat_data)
            markup = await edit_chat_get_keyboard(id)
            await state.finish()
            await bot.edit_message_text(chat_id=chat_id,
                                        message_id=message_id,
                                        text=text,
                                        reply_markup=markup)
            return

        data['type'] = callback_data['type']

        types = await get_types()
        for chat_type in types:
            if chat_type['type'] == data['type']:
                answer = list(chat_type['fields'].values())[0]
                data['params_text'] = chat_type['fields']
                data['params'] = dict()

    await ChatTypeParams.next()
    await bot.send_message(chat_id, f'Enter {answer}:')


# Edit chat: enter params
async def edit_chat_params(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        key = list(data['params_text'].keys())[len(data['params'])]
        data['params'][key] = message.text
        if len(data['params']) >= len(data['params_text'].keys()):
            id = data['id']
            params = {
                'type': data['type'],
                'params': data['params']
            }
            json_resp = await put_chat(id, params)
            await state.finish()
            if json_resp['status'] == 'ok':
                chat_data = await get_chat_by_id(id)
                text = await chat_info(chat_data)
                markup = await edit_chat_get_keyboard(id)
                await bot.send_message(message.from_user.id,
                                       text,
                                       reply_markup=markup)
            else:
                err = json_resp['error']
                await bot.send_message(message.from_user.id,
                                       f'Something went wrong: {err}')
        else:
            answer = list(data['params_text'].values())[len(data['params'])]
            await bot.send_message(message.from_user.id, f'Enter {answer}:')


# Creating notifier: enter name
async def create_notifier_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        data['targets'] = set()

    await Notifier.next()
    markup = await notifier_chats_get_keyboard()
    await bot.send_message(message.from_user.id,
                           'Select chats for notifications:',
                           reply_markup=markup)


# Creating notifier: select chats
async def create_notifier_chats(query: types.CallbackQuery, state: FSMContext,
                                callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id

    async with state.proxy() as data:
        if callback_data['action'] == 'add':
            id = int(callback_data['target'])
            if id in data['targets']:
                data['targets'].remove(id)
            else:
                data['targets'].add(id)
        elif callback_data['action'] == 'create':
            await Notifier.next()
            markup = await notifier_enable_get_keyboard()
            await bot.edit_message_text(chat_id=chat_id,
                                        message_id=message_id,
                                        text='Enable new notifier?',
                                        reply_markup=markup)
            return

        page = int(callback_data['page'])
        markup = await notifier_chats_get_keyboard(page, data['targets'])
        await bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=markup)


# Creating notifier: select is_enabled
async def create_notifier_enabled(query: types.CallbackQuery,
                                  state: FSMContext,
                                  callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    is_enabled = bool(callback_data['enabled'])

    async with state.proxy() as data:
        data['is_enabled'] = is_enabled
        params = {
            'name': data['name'],
            'is_enabled': data['is_enabled'],
            'targets': list(data['targets'])
        }
        json_resp = await post_notifier(params)
        await state.finish()
        if json_resp['status'] == 'ok':
            id = json_resp['id']
            chat_data = await get_notifier_by_id(id)
            text = await notifier_info(chat_data)
            markup = await edit_notifier_get_keyboard(id)
            await bot.edit_message_text(chat_id=chat_id,
                                        message_id=message_id,
                                        text=text,
                                        reply_markup=markup)
        else:
            err = json_resp['error']
            await bot.send_message(chat_id,
                                   f'Something went wrong: {err}')


# Edit notifier: name
async def edit_notifier_name(message: types.Message, state: FSMContext):
    chat_id = message.chat.id

    async with state.proxy() as data:
        id = data['id']

    params = {'name': message.text}
    json_resp = await put_notifier(id, params)

    await state.finish()

    if json_resp['status'] == 'ok':
        notifier_data = await get_notifier_by_id(id)
        text = await notifier_info(notifier_data)
        markup = await edit_notifier_get_keyboard(id)
        await bot.send_message(chat_id,
                               text,
                               reply_markup=markup)
    else:
        err = json_resp['error']
        await bot.send_message(chat_id,
                               f'Something went wrong: {err}')


# Edit notifier: select chats
async def edit_notifier_chats(query: types.CallbackQuery, state: FSMContext,
                              callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id

    async with state.proxy() as data:
        if callback_data['action'] == 'add':
            id = int(callback_data['target'])
            if id in data['targets']:
                data['targets'].remove(id)
            else:
                data['targets'].add(id)
        elif callback_data['action'] == 'create':
            id = data['id']
            params = {'targets': list(data['targets'])}
            json_resp = await put_notifier(id, params)

            await state.finish()

            if json_resp['status'] == 'ok':
                notifier_data = await get_notifier_by_id(id)
                text = await notifier_info(notifier_data)
                markup = await edit_notifier_get_keyboard(id)
                await bot.edit_message_text(chat_id=chat_id,
                                            message_id=message_id,
                                            text=text,
                                            reply_markup=markup)
            else:
                err = json_resp['error']
                await bot.send_message(chat_id,
                                       f'Something went wrong: {err}')
            return

        page = int(callback_data['page'])
        markup = await notifier_chats_get_keyboard(page, data['targets'])
        await bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=markup)


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    logging.warning('Shutting down..')
    await bot.delete_webhook()

    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')


async def init_func():
    if LOGS == 'DEBUG':
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    dp.register_message_handler(start, commands=['start'], chat_id=ADMIN_ID)
    dp.register_message_handler(cancel, state='*', commands='cancel',
                                chat_id=ADMIN_ID)
    dp.register_message_handler(cancel, Text(equals='cancel',
                                             ignore_case=True), state='*')
    dp.register_callback_query_handler(main,
                                       main_callback.filter(
                                           menu=['chats', 'notifiers']),
                                       chat_id=ADMIN_ID)
    dp.register_callback_query_handler(chats, chats_callback.filter(
                                       action=['goto', 'create',
                                               'back', 'open']),
                                       chat_id=ADMIN_ID)
    dp.register_callback_query_handler(edit_chat, edit_chat_callback.filter(
                                       action=['name', 'type', 'delete',
                                               'params', 'back']),
                                       chat_id=ADMIN_ID)
    dp.register_callback_query_handler(notifiers, notifiers_callback.filter(
                                       action=['goto', 'create',
                                               'back', 'open']),
                                       chat_id=ADMIN_ID)
    dp.register_callback_query_handler(edit_notifier,
                                       edit_notifier_callback.filter(
                                        action=['name', 'is_enabled', 'delete',
                                                'chats', 'back']),
                                       chat_id=ADMIN_ID)
    dp.register_callback_query_handler(create_chat_type,
                                       chats_types_callback.filter(),
                                       state=Chat.type, chat_id=ADMIN_ID)
    dp.register_message_handler(create_chat_name, state=Chat.name,
                                chat_id=ADMIN_ID)
    dp.register_message_handler(create_chat_params, state=Chat.params,
                                chat_id=ADMIN_ID)
    dp.register_message_handler(edit_chat_name, state=ChatName.id,
                                chat_id=ADMIN_ID)
    dp.register_callback_query_handler(edit_chat_type,
                                       chats_types_callback.filter(),
                                       state=ChatTypeParams.type,
                                       chat_id=ADMIN_ID)
    dp.register_message_handler(edit_chat_params, state=ChatTypeParams.params,
                                chat_id=ADMIN_ID)
    dp.register_message_handler(create_notifier_name, state=Notifier.name,
                                chat_id=ADMIN_ID)
    dp.register_callback_query_handler(create_notifier_chats,
                                       notifier_chats_callback.filter(),
                                       state=Notifier.targets,
                                       chat_id=ADMIN_ID)
    dp.register_callback_query_handler(create_notifier_enabled,
                                       notifiers_enabled_callback.filter(),
                                       state=Notifier.is_enabled,
                                       chat_id=ADMIN_ID)
    dp.register_message_handler(edit_notifier_name, state=NotifierEdit.id,
                                chat_id=ADMIN_ID)
    dp.register_callback_query_handler(edit_notifier_chats,
                                       notifier_chats_callback.filter(),
                                       state=NotifierEdit.targets,
                                       chat_id=ADMIN_ID)

    app = web.Application()
    executor = Executor(dp, skip_updates=True)
    executor.on_startup(on_startup)
    executor.on_shutdown(on_shutdown)
    executor._prepare_webhook(WEBHOOK_PATH, app=app)
    await executor._startup_webhook()
    return app
