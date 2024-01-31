from aiogram.types import URLInputFile, MessageEntity
from aiogram.utils.markdown import hbold
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, Router, types
import re
import requests
import sys
import logging
import asyncio
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

API_TOKEN = config["API"]["TOKEN"]


#! # All handlers should be attached to the Dispatcher
dp = Dispatcher()

print(API_TOKEN)


@dp.message()
async def message_handler(message: types.Message):
    await message.answer(f"Привет! Отправь мне ссылку на TikTok")


@dp.message()
async def url_handler(message: types.Message):
    url = message
    entities = message.entities
    for entity in entities:
        if entity.type == MessageEntity.URL:
            print('ссылка')
            get_tiktok_video_id(url)
            tiktok(url)

def get_tiktok_video_id(url):

    match = re.search(r'/video/(\d+)', url)
    if match:
        return match.group(1)


def tiktok(url):
    response = requests.get(url)

    video_id = get_tiktok_video_id(response.url)
    print(response.url)

    response = requests.get(f'https://tikcdn.io/ssstik/{video_id}')

    if response.status_code == 200:

        print("Success! Video downloaded.")
        with open(f"{video_id}.mp4", "wb") as file:
            file.write(response.content)
    else:
        print(f"Failed to download video. Status code: {response.status_code}")
        return None


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(API_TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


# Пример использования
# tiktok("https://vm.tiktok.com/ZM6sMUtes/")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
