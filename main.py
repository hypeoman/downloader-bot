import configparser

config = configparser.ConfigParser()
config.read("config.ini")

API_TOKEN = config["API"]["TOKEN"]

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

#! # All handlers should be attached to the Dispatcher
dp = Dispatcher()

print(API_TOKEN)

@dp.message()
async def message_handler(message: types.Message):
    await message.answer(f"Hello!")

async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(API_TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())