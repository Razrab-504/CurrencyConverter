import telebot
from telebot import types
from currency_converter import CurrencyConverter

money = None
values = None

currency = CurrencyConverter()

token = "7869731884:AAG35BNm9if41n2U1Iy656YgtnYJMfUYvaA"
bot = telebot.TeleBot(token=token)

@bot.message_handler(commands=['start', 'konvert'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("100", callback_data="100")
    btn2 = types.InlineKeyboardButton("500", callback_data="500")
    btn3 = types.InlineKeyboardButton("1000", callback_data="1000")
    btn4 = types.InlineKeyboardButton("Ввести сумму", callback_data="self")

    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(message.chat.id, "Я конвертирую валюту по актуальному курсу! Введи сумму и выбери валюты, и я быстро сделаю расчёт. 💱✨", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.isdigit() or call.data == "self")
def amount(call):
    global money
    if call.data.isdigit():
        money = int(call.data)  
        choose_currency(call.message)  # Теперь сразу выбираем валюту
    else:
        bot.send_message(call.message.chat.id, "Введите любую сумму...")
        bot.register_next_step_handler(call.message, konvert)

def konvert(message):
    global money  
    try:
        money = int(message.text.strip())
        choose_currency(message)
    except ValueError:
        bot.send_message(message.chat.id, "Ошибка! Введите число.")
        bot.register_next_step_handler(message, konvert)

def choose_currency(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("USD/EUR", callback_data="USD/EUR")
    btn2 = types.InlineKeyboardButton("USD/EUR", callback_data="USD/EUR")
    btn3 = types.InlineKeyboardButton("RUB/EUR", callback_data="RUB/EUR")
    btn4 = types.InlineKeyboardButton("Ввести валютную пару", callback_data="some")

    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, f"Хорошо, вы ввели сумму {money}. Теперь выберите валютную пару 💵💸", reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def konverter(callback):
    global money
    if callback.data != "some":
        values = callback.data.split('/')
        summ = currency.convert(money, values[0], values[1])
        bot.send_message(callback.message.chat.id, f"Вот ответ: {money} {values[0]} = {summ:.2f} {values[1]} 💵💸. Можете снова ввести сумму.")
        start(callback.message)
    else:
        bot.send_message(callback.message.chat.id, "Введите валютную пару 💵💸")
        bot.register_next_step_handler(callback.message, valutes)

def valutes(message):
    global money
    try:
        value = message.text.strip().split("/")
        if len(value) == 2:
            summ = currency.convert(money, value[0].upper(), value[1].upper())
            bot.send_message(message.chat.id, f"Ваш ответ: {money} {value[0].upper()} = {summ:.2f} {value[1].upper()} 💵💸")
        else:
            bot.send_message(message.chat.id, "Ошибка! Введите валютную пару в формате USD/EUR")
            bot.register_next_step_handler(message, valutes)
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка при конвертации. Проверьте введённые данные.")
        bot.register_next_step_handler(message, valutes)

bot.polling(non_stop=True)
