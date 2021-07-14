from aiohttp import ClientSession

from senders.base import Sender


class Telegram(Sender):
    required_fields = {
        'token': 'Telegram Bot API token',
        'chat_id': 'chat id where notifications will be sent'
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.url = ('https://api.telegram.org/bot{token}/sendMessage'
                    .format(token=self.config['token']))

    async def send(self, message):
        async with ClientSession() as session:
            await session.post(
                self.url,
                params={
                    'chat_id': self.config['chat_id'],
                    'text': message,
                    'parse_mode': 'html'
                }
            )
