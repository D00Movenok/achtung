import typing

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from config import bot
from utils.requests import delete_chat as delete_chat_request
from utils.requests import get_chat_by_id, get_types, post_chat, put_chat
from utils.text import chat_info

from handlers.main.keyboards import get_main_keyboard

from .keyboards import (get_chats_keyboard, get_edit_keyboard,
                        get_types_keyboard)
from .states import ChatCreateState, ChatEditNameState, ChatEditTypeParamsState


async def goto_page(query: types.CallbackQuery,
                    callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    page = int(callback_data['page'])
    markup = await get_chats_keyboard(page)
    await bot.edit_message_reply_markup(chat_id=chat_id,
                                        message_id=message_id,
                                        reply_markup=markup)


async def open_chat(query: types.CallbackQuery,
                    callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    id = callback_data['page']
    chat_data = await get_chat_by_id(id)
    text = await chat_info(chat_data)
    markup = await get_edit_keyboard(id)
    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text=text,
                                reply_markup=markup)


async def create_chat(query: types.CallbackQuery,
                      callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    await ChatCreateState.type.set()
    markup = await get_types_keyboard()
    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text='Select chat type:',
                                reply_markup=markup)


async def go_back_to_main(query: types.CallbackQuery,
                          callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    markup = await get_main_keyboard()
    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text='Select what to do:',
                                reply_markup=markup)


async def edit_name(query: types.CallbackQuery,
                    callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    await ChatEditNameState.id.set()
    state = Dispatcher.get_current().current_state()
    await state.update_data(id=int(callback_data['id']))
    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text='Enter new chat name:')


async def edit_type(query: types.CallbackQuery,
                    callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    await ChatEditTypeParamsState.type.set()
    chat_data = await get_chat_by_id(int(callback_data['id']))
    state = Dispatcher.get_current().current_state()
    await state.update_data(id=int(callback_data['id']))
    await state.update_data(type=chat_data['type'])
    markup = await get_types_keyboard()
    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text='Select chat type:',
                                reply_markup=markup)


async def edit_params(query: types.CallbackQuery,
                      callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    await ChatEditTypeParamsState.params.set()
    chat_data = await get_chat_by_id(int(callback_data['id']))
    state = Dispatcher.get_current().current_state()
    async with state.proxy() as data:
        data['id'] = int(callback_data['id'])
        data['type'] = chat_data['type']

        # prepare to get params
        types = await get_types()
        for chat_type in types:
            if chat_type['type'] == chat_data['type']:
                data['params_text'] = chat_type['fields']
                data['params'] = dict()
        answer = list(data['params_text'].values())[0]
        await bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=f'Enter {answer}:')


async def delete_chat(query: types.CallbackQuery,
                      callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    json_resp = await delete_chat_request(int(callback_data['id']))
    if json_resp['status'] == 'ok':
        markup = await get_chats_keyboard()
        await bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text='Chats menu:',
                                    reply_markup=markup)
    else:
        err = json_resp['error']
        await bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=f'Something went wrong: {err}')


async def go_back_to_chat(query: types.CallbackQuery,
                          callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    markup = await get_chats_keyboard()
    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text='Chats menu:',
                                reply_markup=markup)


async def create_chat_type_state(query: types.CallbackQuery, state: FSMContext,
                                 callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id

    async with state.proxy() as data:
        data['type'] = callback_data['type']

    await ChatCreateState.next()
    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text='Enter new chat name:')


async def create_chat_name_state(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        types = await get_types()
        for chat_type in types:
            if chat_type['type'] == data['type']:
                answer = list(chat_type['fields'].values())[0]
                data['params_text'] = chat_type['fields']
                data['params'] = dict()

    await ChatCreateState.next()
    await bot.send_message(message.from_user.id, f'Enter {answer}:')


async def create_chat_params_state(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        key = list(data['params_text'].keys())[len(data['params'])]
        data['params'][key] = message.text
        if len(data['params']) >= len(data['params_text'].keys()):
            # all params entered
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
                markup = await get_edit_keyboard(json_resp['id'])
                await bot.send_message(message.from_user.id,
                                       text,
                                       reply_markup=markup)
            else:
                err = json_resp['error']
                await bot.send_message(message.from_user.id,
                                       f'Something went wrong: {err}')
        else:
            # enter params
            answer = list(data['params_text'].values())[len(data['params'])]
            await bot.send_message(message.from_user.id, f'Enter {answer}:')


async def edit_chat_name_state(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        params = {'name': message.text}
        id = data['id']

    ans = await put_chat(id, params)

    await state.finish()
    if ans['status'] == 'ok':
        chat_data = await get_chat_by_id(id)
        text = await chat_info(chat_data)
        markup = await get_edit_keyboard(id)
        await bot.send_message(message.from_user.id,
                               text,
                               reply_markup=markup)
    else:
        err = ans['error']
        await bot.send_message(message.from_user.id,
                               f'Something went wrong: {err}')


async def edit_chat_type_state(query: types.CallbackQuery, state: FSMContext,
                               callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id

    async with state.proxy() as data:
        # old type == new type
        if data['type'] == callback_data['type']:
            id = data['id']
            chat_data = await get_chat_by_id(id)
            text = await chat_info(chat_data)
            markup = await get_edit_keyboard(id)
            await state.finish()
            await bot.edit_message_text(chat_id=chat_id,
                                        message_id=message_id,
                                        text=text,
                                        reply_markup=markup)
            return

        # chaning type
        data['type'] = callback_data['type']
        # prepare to get params for new type
        types = await get_types()
        for chat_type in types:
            if chat_type['type'] == data['type']:
                answer = list(chat_type['fields'].values())[0]
                data['params_text'] = chat_type['fields']
                data['params'] = dict()

    await ChatEditTypeParamsState.next()
    await bot.send_message(chat_id, f'Enter {answer}:')


async def edit_chat_params_state(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        key = list(data['params_text'].keys())[len(data['params'])]
        data['params'][key] = message.text
        if len(data['params']) >= len(data['params_text'].keys()):
            # all params entered
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
                markup = await get_edit_keyboard(id)
                await bot.send_message(message.from_user.id,
                                       text,
                                       reply_markup=markup)
            else:
                err = json_resp['error']
                await bot.send_message(message.from_user.id,
                                       f'Something went wrong: {err}')
        else:
            # enter params
            answer = list(data['params_text'].values())[len(data['params'])]
            await bot.send_message(message.from_user.id, f'Enter {answer}:')
