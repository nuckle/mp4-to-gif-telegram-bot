import logging
import ffmpy3

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import NetworkError
from config import TG_TOKEN, FOLDER, GIF_PARAMS


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)


async def convert_video(file_path, file_id):
	"""
	Downloads and converts .mp4 to .mp3
	"""
	await bot.download_file(file_path, FOLDER+file_id+'.mp4')
	ff = ffmpy3.FFmpeg(
	  inputs = {FOLDER+file_id+'.mp4' : None},
	  outputs = {FOLDER+file_id+'.gif' : GIF_PARAMS}
   )
	ff.run()



@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
	"""
	This handler will be called when user sends `/start` command
	"""
	await message.answer("Hi! I can convert .mp4 to .gif")


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
	"""
	This handler will be called when user sends `/help` command
	"""
	await message.answer('Send a video file')


@dp.message_handler(content_types=types.ContentType.VIDEO)
async def send_gif(message: types.Message):
	"""
	This handler will be called when user sends video file
	"""
	file_id = message.video.file_id
	file = await bot.get_file(file_id)
	await message.answer('Processing...')
	await convert_video(file.file_path, file_id)

	await bot.send_chat_action(message.chat.id, 'upload_document')
	try:
		await message.reply_animation(animation=open(FOLDER+file_id+'.gif', 'rb'))
	except NetworkError:
		await message.reply('File is too large')


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
