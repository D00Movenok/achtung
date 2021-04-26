from senders.discord import Discord
from senders.telegram import Telegram

mapper = dict()
# register new senders
mapper['telegram'] = Telegram
mapper['discord'] = Discord
