# pip install pyTelegramBotAPI

from telebot.async_telebot import AsyncTeleBot
import asyncio
import requests

bot = AsyncTeleBot('5693795057:AAEvArS1Hu4cSQjDfDwRytNclskIalrZhuM')


@bot.message_handler(commands=['start'])
async def start_message(message):
    await bot.send_message(message.chat.id, """👋 Привет!

💎 С помощью этого бота ты сможешь узнавать курсы USDT на следующих биржах:
- Binance P2P Тинькофф
- Garantex""")


@bot.message_handler(commands=['get_rates'])
async def send_rates(message):
    binance_rate = get_binance_rates()
    garantex_rate = get_garantex_rates()

    await bot.send_message(message.chat.id, f"""Курсы валют

- Binance Tinkoff {binance_rate}
- Garantex {garantex_rate}""")


def get_binance_rates():
    url = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'

    headers = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }

    params = {
        "proMerchantAds": False,
        "page": 1, "rows": 10,
        "payTypes": ["TinkoffNew"],
        "countries": [],
        "publisherType": None,
        "fiat": "RUB",
        "tradeType": "BUY",
        "asset": "USDT",
        "merchantCheck": False,
        "transAmount": "100000",
    }

    response = requests.post(url=url, headers=headers, json=params).json()
    return response['data'][0]['adv']['price']


def get_garantex_rates():
    url = 'https://garantex.io/api/v2/depth?market=usdtrub'

    response = requests.get(url=url).json()
    return response['asks'][0]['price']


if __name__ == '__main__':
    asyncio.run(bot.polling())