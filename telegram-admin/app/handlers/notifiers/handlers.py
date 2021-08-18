import typing

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from config import bot
from keyboards import (edit_notifier_get_keyboard, main_get_keyboard,
                       notifier_chats_get_keyboard,
                       notifier_enable_get_keyboard, notifiers_get_keyboard)
from utils.requests import (delete_notifier, get_notifier_by_id, post_notifier,
                            put_notifier)
from utils.text import notifier_info

from .states import Notifier, NotifierEdit


async def goto_page(query: types.CallbackQuery,
                    callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    page = int(callback_data['page'])
    markup = await notifiers_get_keyboard(page)
    await bot.edit_message_reply_markup(chat_id=chat_id,
                                        message_id=message_id,
                                        reply_markup=markup)


async def open_notifier(query: types.CallbackQuery,
                        callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    id = callback_data['page']
    notifier_data = await get_notifier_by_id(id)
    text = await notifier_info(notifier_data)
    markup = await edit_notifier_get_keyboard(id)
    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text=text,
                                reply_markup=markup)


async def create_notifier(query: types.CallbackQuery,
                          callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    await Notifier.name.set()
    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text='Enter new notifier name:')


async def back_to_main(query: types.CallbackQuery,
                       callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    markup = await main_get_keyboard()
    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text='Select what to do:',
                                reply_markup=markup)


async def edit_name(query: types.CallbackQuery,
                    callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    await NotifierEdit.id.set()
    state = Dispatcher.get_current().current_state()
    await state.update_data(id=int(callback_data['id']))
    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text='Enter new notifier name:')


async def edit_is_enabled(query: types.CallbackQuery,
                          callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id
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


async def edit_chats(query: types.CallbackQuery,
                     callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id
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


async def del_notifier(query: types.CallbackQuery,
                       callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id
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


async def back_to_notifiers(query: types.CallbackQuery,
                            callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    markup = await notifiers_get_keyboard()
    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text='Notifiers menu:',
                                reply_markup=markup)   


async def create_notifier_name_state(message: types.Message,
                                     state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        data['targets'] = set()

    await Notifier.next()
    markup = await notifier_chats_get_keyboard()
    await bot.send_message(message.from_user.id,
                           'Select chats for notifications:',
                           reply_markup=markup)


async def create_notifier_chats_state(query: types.CallbackQuery,
                                      state: FSMContext,
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


async def create_notifier_enabled_state(query: types.CallbackQuery,
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


async def edit_notifier_name_state(message: types.Message, state: FSMContext):
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


async def edit_notifier_chats_state(query: types.CallbackQuery,
                                    state: FSMContext,
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
