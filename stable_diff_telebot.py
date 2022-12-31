# Новогодняя аватарка с помощью нейросети в стиле GTA 5 - Телеграм бот на Python

# Подписывайтесь, чтобы
# быстрее узнавать о
# новых уроках - https://t.me/isartem_bot

# pip install pyTelegramBotAPI

from config import *
from telebot.async_telebot import AsyncTeleBot
import asyncio
import requests
import ftplib

bot = AsyncTeleBot(telebot_api_key)
ftp_server = ftplib.FTP(ftp_hostname, ftp_username, ftp_password)


@bot.message_handler(commands=['start'])
async def start_message(message):
    await bot.send_message(message.chat.id, """👋 Привет!

❄️ Этот бот создан для генерации новогодних изображений с помощью искусственного интеллекта ☃️""")


@bot.message_handler(content_types=['photo'])
async def handle_photos(message):
    await bot.send_message(message.chat.id, '🪫 Скачиваю изображение')

    photo_id = message.photo[-1].file_id
    photo_info = await bot.get_file(photo_id)
    downloaded_img = await bot.download_file(photo_info.file_path)
    with open("img_for_upload.jpg", "wb") as code:
        code.write(downloaded_img)

    await bot.send_message(message.chat.id, '🔋 Изображение подготовлено для обработки, сохраняю в файловое хранилище')

    with open("img_for_upload.jpg", "rb") as file:
        ftp_server.storbinary(f"STOR img_for_upload.jpg", file)

    await bot.send_message(message.chat.id, f'⏳ Отправляю в нейросеть')

    data = {
        "key": stable_diff_api_key,
        "model_id": "midjourney",
        "prompt": "happy new year style, christmas trees, snow, Gta vice city, gta 5 cover art, borderlands style, celshading, symmetric highly detailed eyes, trending on artstation, by rhads, andreas rocha, rossdraws, makoto shinkai, laurie greasley",
        "negative_prompt": "extra fingers, mutated hands, poorly drawn hands, poorly drawn face, deformed, ugly, blurry, bad anatomy, bad proportions, extra limbs, cloned face, skinny, glitchy, double torso, extra arms, extra hands, mangled fingers, missing lips, ugly face, distorted face, extra legs, anime",
        "init_image": "https://bot.margelet.org/storage/img_for_upload.jpg",
        "width": "504",
        "height": "504",
        "samples": "1",
        "scheduler": None,
        "num_inference_steps": "30",
        "guidance_scale": 7.5,
        "strength": 0.7,
        "seed": None,
        "webhook": None,
        "track_id": None,
    }

    response = requests.post(url='https://stablediffusionapi.com/api/v4/dreambooth/img2img', json=data).json()

    if response['status'] == 'success' and len(response['output']) > 0:
        image_url = response['output'][0]

        await bot.send_photo(message.chat.id, image_url)
    else:
        await bot.send_message(message.chat.id, '🎈 Ошибка обработки изображения')


if __name__ == '__main__':
    asyncio.run(bot.polling())
