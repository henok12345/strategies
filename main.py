import os, telebot
from telebot import types
from pepper_fix import PepperstoneFIX
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))
engine = PepperstoneFIX()

@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🔗 Connect FIX", callback_data="connect"),
        types.InlineKeyboardButton("🚀 Buy Gold", callback_data="buy"),
        types.InlineKeyboardButton("🛑 Kill Switch", callback_data="kill")
    )
    bot.reply_to(message, "🦅 *PEPPERSTONE COMMANDER*\nAccount: 5244103\nStatus: Online & Ready", 
                 parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "connect":
        status = engine.connect()
        bot.send_message(call.message.chat.id, status)
    elif call.data == "buy":
        res = engine.buy_gold()
        bot.send_message(call.message.chat.id, res)

bot.infinity_polling()
