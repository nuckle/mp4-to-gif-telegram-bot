import logging
import sys
import asyncio

import ffmpy3

from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import FSInputFile
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.methods import SendAnimation
from aiogram.exceptions import TelegramNetworkError
from config import TG_TOKEN, FOLDER, GIF_PARAMS


# Initialize dispatcher, bot and router

dp = Dispatcher()
router = Router()
bot = Bot(TG_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def convert_video(file_path, file_id):
    """
    Downloads and converts .mp4 to .mp3
    """
    await bot.download_file(file_path, FOLDER + file_id + ".mp4")
    ff = ffmpy3.FFmpeg(
        inputs={FOLDER + file_id + ".mp4": None},
        outputs={FOLDER + file_id + ".gif": GIF_PARAMS},
    )
    ff.run()


@dp.message(CommandStart())
async def send_welcome(message: types.Message) -> None:
    """
    This handler will be called when user sends `/start` command
    """
    await message.answer("Hi! I can convert .mp4 to .gif")


@router.message(Command("help"))
async def send_help(message: types.Message):
    """
    This handler will be called when user sends `/help` command
    """
    await message.answer("Send a video file")


@router.message(F.content_type.in_({"video"}))
async def send_gif(message: types.Message):
    """
    This handler will be called when user sends video file
    """
    file_id = message.video.file_id
    file = await bot.get_file(file_id)
    await message.answer("Processing...")
    await convert_video(file.file_path, file_id)
    await bot.send_chat_action(message.chat.id, "upload_document")
    try:
        # await message.reply_animation(animation=open(FOLDER+file_id+'.gif', 'rb'))
        gif = FSInputFile(FOLDER + file_id + ".gif")
        await bot(SendAnimation(chat_id=message.chat.id, animation=gif))
    except TelegramNetworkError:
        await message.reply("File is too large")


async def main() -> None:
    dp.include_router(router)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
