import os
from flask import Flask
from threading import Thread
import telebot
from telebot import types

# Токен вашего бота
TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)
bot = telebot.TeleBot(TOKEN)

# Настройка Flask для удовлетворения требований Render к портам
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is active and running!"

def run_web():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# Запуск Flask-сервера в фоновом потоке
Thread(target=run_web).start()

# Стек языковых сообщений
MESSAGES = {
    'uk': {
        'welcome': (
            "Вітаю! 🤍 Ласкаво просимо до мого творчого простору.\n\n"
            "Я створюю сучасні сайти, Telegram-боти "
            "та допомагаю брендам заявляти про себе стильно й елегантно.\n\n"
            "Оберіть зручну мову для продовження:"
        ),
        'chosen': "Чудово! Ви обрали українську мову. Оберіть потрібний розділ нижче 👇",
        'btn_services': "💼 Послуги та ціни",
        'btn_contact': "✨ З'єднатися",
    },
    'ru': {
        'welcome': (
            "Здравствуйте! 🤍 Добро пожаловать в мое творческое пространство.\n\n"
            "Я создаю современные сайты, Telegram-боты "
            "и помогаю брендам заявлять о себе стильно и элегантно.\n\n"
            "Выберите удобный язык для продолжения:"
        ),
        'chosen': "Отлично! Вы выбрали русский язык. Выберите нужный раздел ниже 👇",
        'btn_services': "💼 Услуги и цены",
        'btn_contact': "✨ Связаться",
    },
    'ro': {
        'welcome': (
            "Salut! 🤍 Bun venit în spațiul meu creativ.\n\n"
            "Creez site-uri moderne, boți de Telegram "
            "și ajut brandurile să se remarce cu stil și eleganță.\n\n"
            "Alegeți limba dorită pentru a continua:"
        ),
        'chosen': "Minunat! Ați ales limba română. Alegeți secțiunea dorită mai jos 👇",
        'btn_services': "💼 Servicii și prețuri",
        'btn_contact': "✨ Conectare",
    }
}

user_languages = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(
        types.InlineKeyboardButton("🇺🇦 UA", callback_data='lang_uk'),
        types.InlineKeyboardButton("🇷🇺 RU", callback_data='lang_ru'),
        types.InlineKeyboardButton("🇷🇴 RO", callback_data='lang_ro')
    )
    bot.send_message(message.chat.id, MESSAGES['uk']['welcome'], reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def set_language(call):
    lang = call.data.split('_')[1]
    user_languages[call.from_user.id] = lang
    
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(
        types.KeyboardButton(MESSAGES[lang]['btn_services']),
        types.KeyboardButton(MESSAGES[lang]['btn_contact'])
    )
    
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, MESSAGES[lang]['chosen'], reply_markup=keyboard)

if __name__ == "__main__":
    bot.infinity_polling()
