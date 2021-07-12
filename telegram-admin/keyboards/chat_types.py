from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from aiohttp import ClientSession
from config import ADMIN_PASS, CATCHER_URL

chats_types_callback = CallbackData('chats', 'type')


async def chats_types_get_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)

    async with ClientSession() as session:
        async with session.get(CATCHER_URL + '/api/chats/types',
                               headers={'X-Admin-Auth': ADMIN_PASS}) as resp:
            for chat_type in await resp.json():
                type_callback_data = chats_types_callback.new(
                    type=chat_type['type']
                )
                markup.add(
                    InlineKeyboardButton(chat_type['type'],
                                         callback_data=type_callback_data)
                )

    return markup
