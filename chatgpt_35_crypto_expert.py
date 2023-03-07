# Телеграм бот на Chat GPT 3.5 Турбо - консультант по трейдингу

# Подписывайтесь, чтобы
# быстрее узнавать о
# новых уроках - https://t.me/isartem_bot

# Мой Boosty с
# доработанными скриптами и другой
# полезной информацией - https://boosty.to/isartem

# pip install aiogram asyncio openai

from config import *
import logging
import openai
from aiogram import Bot, Dispatcher, executor, types

openai.api_key = OPENAI_API_KEY

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)


async def ai(prompt):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": 'Тебя зовут Артем и ты являешься экспертом по торговле криптовалютами, который будет консультировать пользователей по вопросам, связанным с трейдингом на различных биржах.'},
                {"role": "user", "content": prompt}
            ]
        )

        return completion.choices[0].message.content
    except:
        return None


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я эксперт по торговле криптовалютами, что Вас интересует?")



@dp.message_handler()
async def echo(message: types.Message):
    answer = await ai(message.text)

    if answer != None:
        await message.reply(answer)
    else:
        await message.reply('😞 Неизвестная ошибка, попробуйте еще раз')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)