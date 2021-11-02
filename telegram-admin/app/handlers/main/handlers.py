import typing

from aiogram import types
from aiogram.dispatcher import FSMContext
from config import bot

from handlers.chats.keyboards import get_chats_keyboard
from handlers.notifiers.keyboards import get_notifiers_keyboard

from .keyboards import get_main_keyboard


async def start(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Select what to do:',
                           reply_markup=await get_main_keyboard())


async def get_id(message: types.Message):
    await bot.send_message(message.chat.id,
                           message.chat.id)


# cansel any state
async def cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(message.from_user.id,
                           'Cancelled.',
                           reply_markup=types.ReplyKeyboardRemove())


async def goto_chats(query: types.CallbackQuery,
                     callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    markup = await get_chats_keyboard()
    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text='Chats menu:',
                                reply_markup=markup)


async def goto_notifiers(query: types.CallbackQuery,
                         callback_data: typing.Dict[str, str]):
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    markup = await get_notifiers_keyboard()
    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text='Notifiers menu:',
                                reply_markup=markup)
