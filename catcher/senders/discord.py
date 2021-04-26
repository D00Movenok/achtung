from aiohttp import ClientSession

from senders.base import Sender


class Discord(Sender):
    required_fields = {
        'token': 'discord bot api token',
        'channel_id': 'channel id where notifications will be sent'
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.url = ('https://discordapp.com/api/channels/{channel}/messages'
                    .format(channel=self.config['channel_id']))

    async def send(self, message):
        async with ClientSession() as session:
            await session.post(
                self.url,
                headers={
                    'Authorization': f'Bot {self.config["token"]}'
                },
                json={
                    'content': message
                }
            )
