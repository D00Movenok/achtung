import os
from aiogram import Bot

API_TOKEN = os.environ['API_TOKEN']
CATCHER_URL = os.environ['CATCHER_URL']
PAGE_LIMIT = int(os.environ['PAGE_LIMIT'])
ADMIN_PASS = os.environ['ADMIN_PASS']
ADMIN_ID = os.environ['ADMIN_ID'].split(',')
LOGS = os.environ['LOGS']
WEBHOOK_PATH = os.environ['WEBHOOK_PATH']
WEBHOOK_HOST = os.environ['WEBHOOK_HOST']

bot = Bot(token=API_TOKEN)
