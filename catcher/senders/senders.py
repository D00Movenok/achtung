from senders.discord import Discord
from senders.telegram import Telegram

mapper = dict()
# register new senders
mapper['Telegram'] = Telegram
mapper['Discord'] = Discord
