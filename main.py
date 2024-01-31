from aiogram.utils.markdown import hbold
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, Router, types
from aiogram import F
from aiogram.types import FSInputFile
from pytube import YouTube
from aiogram.types import URLInputFile
import sys
import logging
import asyncio
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

API_TOKEN = config["API"]["TOKEN"]


#! All handlers should be attached to the Dispatcher
dp = Dispatcher()

#! TODO: Write this function
def get_tiktok_video() -> None:
    pass

#! function to get video from youtube
def get_youtube_video(url) -> str:
    youtubeObject = YouTube(url)
    youtubeObject = youtubeObject.streams.filter(
        file_extension="mp4").get_highest_resolution()
    try:
        youtubeObject.download()
        logging.info("Download is completed successfully")
        path = f"{youtubeObject.title}.mp4"
        logging.info(f"Filepath got correctly: {path}")

        return path
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
            filepath = get_youtube_video(url)
            video_to_send = FSInputFile(filepath)
            await message.answer_video(video_to_send)
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

#! TODO
def translate_to_selected_language(text) -> str:
    pass

#! /start command handler
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, I can download videos from tiktok, youtube, youtube shorts and reels!")

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
