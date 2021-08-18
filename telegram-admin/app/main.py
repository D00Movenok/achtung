import logging

from aiogram import Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import Executor
from aiohttp import web

from config import LOGS, WEBHOOK_HOST, WEBHOOK_PATH, bot
from handlers import register_chats, register_main, register_notifiers

WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 8080


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    logging.warning('Shutting down..')
    await bot.delete_webhook()

    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')


def register_all_handlers(dp: Dispatcher):
    register_main(dp)
    register_chats(dp)
    register_notifiers(dp)


async def init_func():
    if LOGS == 'DEBUG':
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    register_all_handlers(dp)

    app = web.Application()
    executor = Executor(dp, skip_updates=True)
    executor.on_startup(on_startup)
    executor.on_shutdown(on_shutdown)
    executor._prepare_webhook(WEBHOOK_PATH, app=app)
    await executor._startup_webhook()
    return app


if __name__ == '__main__':
    if LOGS == 'DEBUG':
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    register_all_handlers(dp)
    executor.start_polling(dp)
