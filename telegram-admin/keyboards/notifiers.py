from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from aiohttp import ClientSession
from config import ADMIN_PASS, CATCHER_URL, PAGE_LIMIT

notifiers_callback = CallbackData('notifiers', 'action', 'page')


async def notifiers_get_keyboard(page: int = 0):
    markup = InlineKeyboardMarkup(row_width=3)

    previous_callback_data = notifiers_callback.new(action='goto',
                                                    page=page-1)
    page_callback_data = notifiers_callback.new(action='page', page=page)
    next_callback_data = notifiers_callback.new(action='goto', page=page+1)
    create_callback_data = notifiers_callback.new(action='create', page=page)
    back_callback_data = notifiers_callback.new(action='back', page=page)

    async with ClientSession() as session:
        async with session.get(CATCHER_URL + '/api/notifiers', params={
            'limit': PAGE_LIMIT,
            'offset': page
        }, headers={'X-Admin-Auth': ADMIN_PASS}) as resp:
            is_max = len(await resp.json()) == PAGE_LIMIT
            for notifier in await resp.json():
                open_callback_data = notifiers_callback.new(
                    action='open',
                    page=notifier['id']
                )
                markup.add(
                    InlineKeyboardButton(notifier['name'],
                                         callback_data=open_callback_data)
                )
        if is_max:
            async with session.get(CATCHER_URL + '/api/notifiers', params={
                'limit': PAGE_LIMIT,
                'offset': page + 1
            }, headers={
                'X-Admin-Auth': ADMIN_PASS
            }) as resp:
                is_next = len(await resp.json()) > 0
        else:
            is_next = False

    pagination = []
    if page > 0:
        pagination.append(
            InlineKeyboardButton('<', callback_data=previous_callback_data)
        )
    if is_next or page > 0:
        pagination.append(
            InlineKeyboardButton('Page', callback_data=page_callback_data)
        )
    if is_next:
        pagination.append(
            InlineKeyboardButton('>', callback_data=next_callback_data)
        )

    markup.row(*pagination)
    markup.add(
        InlineKeyboardButton('Create', callback_data=create_callback_data)
    )
    markup.add(
        InlineKeyboardButton('Back', callback_data=back_callback_data)
    )

    return markup
