from aiogram.utils.markdown import hbold
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, Router, types
from aiogram import F
from aiogram.types import FSInputFile
from aiogram.types import URLInputFile
from requests import get
from json import loads
import mysql.connector
import yt_dlp
import sys
import logging
import asyncio
import configparser
import os

config = configparser.ConfigParser()
config.read("config.ini")

API_TOKEN = config["API"]["TOKEN"]


# * All handlers should be attached to the Dispatcher
dp = Dispatcher()


# * function to get video (not from inst)
def get_youtube_video(url, output_dir):
    ydl_opts = {
        'format': 'best',
        'outtmp': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'restrict-filenames': True,
        'max_filesize': 350 * 1024 * 1024,
        'max_duration': 1800
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            return os.path.join(output_dir, ydl.prepare_filename(info))
        except yt_dlp.utils.DownloadError as e:
            logging.error("Download error:" + str(e))

# * function to get video from inst
def get_instagram_video(url, output_dir):
    SESSIONID = 1

# * Url handler
@dp.message(F.text.startswith("https"))
async def url_handler(message: types.Message):
    try:
        url = message.text

        try:
            filepath = get_youtube_video(url, os.getcwd())
            video_to_send = FSInputFile(filepath)
            await message.answer_video(video_to_send)
            os.remove(filepath)
        except:
            pass
    except:
        await message.answer(f'Error downloading video')

#* Instagram url handler
@dp.message(F.text.startswith("https").contains("instagram.com"))
async def instagram_url_handler(message: types.Message):
    try:
        url = message.text
        
        try:
            filepath = get_instagram_video(url, os.getcwd())
            video_to_send = FSInputFile(filepath)
            await message.answer_video(video_to_send)
            os.remove(filepath)
        except:
            pass
    except:
        await message.answer(f'Error downloading video')

# TODO
def translate_to_selected_language(text) -> str:
    pass

# TODO /start command handler
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, I can download videos from tiktok, youtube and many other platforms. \n"
                         + "The full list can be found at this link: \n"
                         + "Select your language using the buttons below:")

# * Main function
async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(API_TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)

# * Start program via main function
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    asyncio.run(main())     