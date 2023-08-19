import telebot
import config
from extenstions import ApiException, Converter

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Шалом!"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for i in config.exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    try:
        base, sym, amount = message.text.split()
    except ValueError as e:
        bot.reply_to(message, "Неверое количество параметров :(")
    try:
        new_price = Converter.get_price(base, sym, amount)
        bot.reply_to(message, f"Цена {amount} {base} в {sym} : {new_price}")
    except ApiException as e:
        bot.reply_to(message, "Ошибка в команде! \n{e}")


bot.polling()
