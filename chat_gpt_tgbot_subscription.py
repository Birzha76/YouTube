# Chat GPT пишет Телеграм бот для общения с ИИ

# Подписывайтесь, чтобы
# быстрее узнавать о
# новых уроках - https://t.me/isartem_bot

# Мой Boosty с
# доработанными скриптами и другой
# полезной информацией - https://boosty.to/isartem

# pip install pyTelegramBotAPI openai

import openai
import telebot

# Set up your OpenAI API credentials
openai.api_key = "YOUR_OPENAI_API_KEY_HERE"

# Set up your Telegram bot API credentials
bot = telebot.TeleBot("YOUR_TELEGRAM_BOT_API_KEY_HERE")

# Define a command handler for the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Type /help to see the available commands.")

# Define a command handler for the /help command
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "You can use the /ask command to ask a question to the OpenAI API.")

# Define a command handler for the /ask command
@bot.message_handler(commands=['ask'])
def send_question(message):
    try:
        # Check if the user is subscribed to the allowed chat
        chat_id = '@isartem'
        user_id = message.from_user.id
        member = bot.get_chat_member(chat_id, user_id)
        if member.status not in ['member', 'administrator', 'creator']:
            bot.reply_to(message, "Sorry, you must be a member of the allowed chat to use this command.")
            return

        # Send a message asking for the user's question
        bot.reply_to(message, "What's your question?")

        # Define a function to handle the user's response
        def handle_question(response):
            try:
                # Call the OpenAI API to get the answer to the question
                result = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=response.text,
                    max_tokens=1024,
                    n=1,
                    stop=None,
                    temperature=0.7,
                )

                # Send the answer back to the user
                bot.reply_to(message, result.choices[0].text)

            except Exception as e:
                # Send an error message if something goes wrong
                bot.reply_to(message, e)

        # Wait for the user's response and handle it with the handle_question function
        bot.register_next_step_handler(message, handle_question)

    except Exception as e:
        # Send an error message if something goes wrong
        bot.reply_to(message, e)


# Start the bot
bot.polling()
