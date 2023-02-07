# Что такое Chat GPT - создаем Телеграм бот для общения с нейросетью OpenAI

# Подписывайтесь, чтобы
# быстрее узнавать о
# новых уроках - https://t.me/isartem_bot

# pip install pyTelegramBotAPI
# pip install openai

import telebot
import openai

bot = telebot.TeleBot("TELEGRAM_BOT_TOKEN")
openai.api_key = "OPENAI_API_KEY"

@bot.message_handler(content_types=["text"])
def handle_text(message):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{message.text}",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    bot.send_message(message.chat.id, response.choices[0].text)

bot.polling()
