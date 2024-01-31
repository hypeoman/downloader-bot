from aiogram.utils.markdown import hbold
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, Router, types
from pytube import YouTube
import sys
import logging
import asyncio
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

API_TOKEN = config["API"]["TOKEN"]
#test

#! All handlers should be attached to the Dispatcher
dp = Dispatcher()

#! TODO: Write this function
def get_tiktok_video() -> None:
    pass

#! TODO: Write this function
def get_youtube_video(url) -> None:
    youtubeObject = YouTube(url)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download()
        logging.info("Download is completed successfully")
    except:
        logging.error("An error has occured while downloading youtube video.")

#! TODO: Write this function
def get_reels_video() -> None:
    pass

#! Url handler
@dp.message()
async def url_handler(message: types.Message):
    #! This hadnler try get videos from:
    #! 1. youtube (with shorts);
    #! 2. tiktok;
    #! 3. reels;
    try:
        url = message.text

        try:
            get_youtube_video(url)
        except:
            try:
                get_tiktok_video(url)
            except:
                try:
                    get_reels_video(url)
                except:
                    pass
    except:
        pass

#! Main message_handler
@dp.message()
async def message_handler(message: types.Message):
    await message.answer(f"Hello!")

#! Main function
async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(API_TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)

#! Start program via main function
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
