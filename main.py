import os
import telebot
from telebot import types

# O Render vai ler esse BOT_TOKEN das configurações que faremos lá
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def boas_vindas(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('🏋️ Registrar Treino')
    btn2 = types.KeyboardButton('🍎 Minha Dieta')
    btn3 = types.KeyboardButton('🤖 Perguntar ao Personal IA')
    markup.add(btn1, btn2, btn3)
    
    bot.send_message(message.chat.id, "E aí! Bora focar no shape hoje?", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def eco(message):
    if message.text == '🏋️ Registrar Treino':
        bot.reply_to(message, "Em breve vamos salvar suas cargas aqui!")
    elif message.text == '🍎 Minha Dieta':
        bot.reply_to(message, "Área de macros em desenvolvimento...")
    elif message.text == '🤖 Perguntar ao Personal IA':
        bot.reply_to(message, "Manda sua dúvida que a IA responde!")

bot.polling()
