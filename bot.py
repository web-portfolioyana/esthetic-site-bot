import os
import threading
from flask import Flask
import telebot
from telebot import types

# Читаємо токен безпечно з налаштувань Render або вставляємо за потреби
TOKEN = os.environ.get("TOKEN", "9121526674:AAFuArIZe2uf579HIwjqq9UAkBE6UQMCn54")

bot = telebot.TeleBot(TOKEN)

# --- Flask сервер для того, щоб Render не вимикав веб-сервіс ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running online!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Тексти трьома мовами
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
        'services_text': (
            "МОЇ ПОСЛУГИ ТА НАПРЯМКИ:\n\n"
            "1. Веб-розробка та сайти:\n"
            "• Створення адаптивних сайтів на HTML/CSS, Tailwind та JavaScript.\n"
            "• Landing page та портфоліо під ключ.\n\n"
            "2. Telegram-боти:\n"
            "• Розробка та налаштування функціональних ботів під ваші завдання (портфоліо, візитки, автоматизація).\n\n"
            "Напишіть мені напряму, щоб обговорити ваш проєкт!"
        ),
        'contact_text': (
            "ЗВ'ЯЗАТИСЯ ЗІ МНОЮ:\n\n"
            "Ви можете обговорити деталі співпраці або замовити проєкт, написавши мені в особисті повідомлення:\n"
            "Telegram: @i_ana333\n"
            "Портфоліо: https://web-portfolioyana.github.io/portfolio/\n\n"
            "Буду рада втілити вашу ідею в життя! 🤍"
        )
    },
    'en': {
        'welcome': (
            "Hello! 🤍 Welcome to my creative space.\n\n"
            "I specialize in modern web development, Telegram bots, "
            "and helping brands shine with style and elegance.\n\n"
            "Please choose your preferred language:"
        ),
        'chosen': "Great! You selected English. Choose a section below 👇",
        'btn_services': "💼 Services & Prices",
        'btn_contact': "✨ Contact me",
        'services_text': (
            "MY SERVICES & EXPERTISE:\n\n"
            "1. Web Development:\n"
            "• Custom responsive websites using HTML/CSS, Tailwind, and JavaScript.\n"
            "• Modern landing pages and portfolios.\n\n"
            "2. Telegram Bots:\n"
            "• Development and setup of functional Telegram bots for your business or portfolio.\n\n"
            "Contact me directly to discuss your project!"
        ),
        'contact_text': (
            "GET IN TOUCH:\n\n"
            "Feel free to reach out to discuss your project or collaboration:\n"
            "Telegram: @i_ana333\n"
            "Portfolio: https://web-portfolioyana.github.io/portfolio/\n\n"
            "Looking forward to creating something beautiful together! 🤍"
        )
    },
    'es': {
        'welcome': (
            "¡Hola! 🤍 Bienvenido/a a mi espacio creativo.\n\n"
            "Me especializo en desarrollo web moderno, bots de Telegram "
            "y en ayudar a las marcas a destacar con elegancia.\n\n"
            "Por favor, elige tu idioma:"
        ),
        'chosen': "¡Genial! Has elegido español. Elige una opción abajo 👇",
        'btn_services': "💼 Servicios y precios",
        'btn_contact': "✨ Contáctame",
        'services_text': (
            "MIS SERVICIOS:\n\n"
            "1. Desarrollo Web:\n"
            "• Sitios web responsivos con HTML/CSS, Tailwind y JavaScript.\n"
            "• Landing pages y portafolios modernos.\n\n"
            "2. Bots de Telegram:\n"
            "• Creación y configuración de bots funcionales para tus proyectos y negocios.\n\n"
            "¡Escríbeme para hablar sobre tu proyecto!"
        ),
        'contact_text': (
            "CONTACTO:\n\n"
            "Puedes contactarme directamente para colaboraciones:\n"
            "Telegram: @i_ana333\n"
            "Portafolio: https://web-portfolioyana.github.io/portfolio/\n\n"
            "¡Será un placer trabajar contigo! 🤍"
        )
    }
}

# Зберігаємо обрану мову для кожного користувача
user_languages = {}

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=3)
    btn_uk = types.InlineKeyboardButton("🇺🇦 UA", callback_data='lang_uk')
    btn_en = types.InlineKeyboardButton("🇬🇧 EN", callback_data='lang_en')
    btn_es = types.InlineKeyboardButton("🇪🇸 ES", callback_data='lang_es')
    markup.add(btn_uk, btn_en, btn_es)
    
    bot.send_message(message.chat.id, MESSAGES['uk']['welcome'], reply_markup=markup)

# Обробка натискання інлайн-кнопок вибору мови
@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def set_language(call):
    lang = call.data.split('_')[1]
    user_languages[call.message.chat.id] = lang  # запам'ятовуємо мову
    text = MESSAGES.get(lang, MESSAGES['en'])
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(text['btn_services']))
    markup.add(types.KeyboardButton(text['btn_contact']))
    
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, text['chosen'], reply_markup=markup)

# Обробка текстових кнопок меню
@bot.message_handler(func=lambda message: True)
def handle_menu_text(message):
    chat_id = message.chat.id
    lang = user_languages.get(chat_id, 'uk')  # за замовчуванням українська
    text_data = MESSAGES.get(lang, MESSAGES['uk'])
    
    if message.text == text_data['btn_services']:
        bot.send_message(chat_id, text_data['services_text'])
    elif message.text == text_data['btn_contact']:
        bot.send_message(chat_id, text_data['contact_text'], disable_web_page_preview=True)
    else:
        bot.send_message(chat_id, "Оберіть потрібний розділ за допомогою кнопок нижче 👇")

if __name__ == "__main__":
    # Запускаємо веб-сервер у фоновому потоці для Render
    web_thread = threading.Thread(target=run_web)
    web_thread.daemon = True
    web_thread.start()
    
    print("Веб-сервер запущено, стартуємо Telegram-бота...")
    
    # Запускаємо бота з автопереподключенням
    while True:
        try:
            bot.infinity_polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Помилка з'єднання з Telegram: {e}")
