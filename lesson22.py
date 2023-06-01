import os
import logging
import random

from aiogram import Bot, Dispatcher, executor, types

from decouple import config

API_TOKEN = config('TELEGRAM_BOT_TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    text = 'Прівіт, радий тебе бачити!\n\n' \
            'Якщо ти хочеш дізнатися, що я вмію, то напиши /help'
    await message.reply(text)

    
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply("Я бот для навчання Python. Поки що я вмію тільки це.")


@dp.message_handler(content_types=['photo'])    
async def photo_handler(message: types.Message):
    # print(message.photo)
    await message.reply_photo(message.photo[-1].file_id)
    await bot.download_file_by_id(message.photo[-1].file_id, f'photos/{message.photo[-1].file_unique_id}_{message.from_user.username}.jpg')
       
@dp.message_handler(commands=['get_photos'])
async def get_photos(message: types.Message):
    list_of_photos = os.listdir('photos')
    print(list_of_photos)
    for photo in list_of_photos:
        name = photo.split('_')[1][:-4]
        with open(f'photos/{photo}', 'rb') as file:
            await message.reply_photo(file, f'Автор: {name}')

@dp.message_handler(commands=['get_media_photo'])
async def get_media_photo(message: types.Message):
    media = types.MediaGroup()
    list_of_photos = os.listdir('photos')
    random.shuffle(list_of_photos)
    for photo in list_of_photos[:10]:
        name = photo.split('_')[1][:-4]
        media.attach_photo(types.InputFile(f'photos/{photo}'),f'Автор: {name}')
    await message.answer_media_group(media=media)
    


@dp.message_handler()
async def echo(message: types.Message):
    if message.text.lower() == 'котик':
        list_of_photos = os.listdir('photos')
        photo = random.choice(list_of_photos)
        await message.answer_photo(types.InputFile(f'photos/{photo}'), caption='Котик')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    

