from typing import Dict

from .requests import get_chat_by_id


async def chat_info(chat_data: Dict):
    text = f'Chat name: {chat_data["name"]}\n'
    text += f'Chat type: {chat_data["type"]}\n'
    text += 'Params:\n'
    for key, value in chat_data['params'].items():
        text += f'-- {key}: {value}\n'

    return text


async def notifier_info(notifier_data: Dict):
    text = f'Notifier name: {notifier_data["name"]}\n'
    text += f'Notifier access token: {notifier_data["access_token"]}\n'
    text += f'Notifier enabled: {notifier_data["is_enabled"]}\n'
    text += 'Targets:\n'
    for id in notifier_data['targets']:
        json_data = await get_chat_by_id(id)
        text += f'-- {json_data["name"]}\n'

    return text
