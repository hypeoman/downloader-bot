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
router = Router()

@router.message()
async def command_start_handler(message: Message) -> Any:
    print(API_TOKEN)
    await message.answer(f"Hello!")

#PISISIS