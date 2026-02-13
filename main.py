import os
import telebot
from telebot import types

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# --- MENUS PRINCIPAIS ---
@bot.message_handler(commands=['start', 'menu'])
def main_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        types.KeyboardButton('🏋️ ÁREA DE TREINO'),
        types.KeyboardButton('🍎 DIETA E MACROS'),
        types.KeyboardButton('🤖 PERSONAL IA'),
        types.KeyboardButton('⚙️ UTILITÁRIOS')
    )
    bot.send_message(message.chat.id, "Fala David! Escolha uma categoria para começar:", reply_markup=markup)

# --- SUBMENUS ---
@bot.message_handler(func=lambda message: True)
def handle_menus(message):
    chat_id = message.chat.id
    text = message.text

    if text == '🏋️ ÁREA DE TREINO':
        m = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        m.add('📝 Registrar Carga', '⏱️ Descanso', '📅 Divisão A/B/C', '📈 Ver Evolução', '🔄 Substituir Exercício', '🔙 Voltar')
        bot.send_message(chat_id, "Foco no peso! O que quer fazer?", reply_markup=m)

    elif text == '🍎 DIETA E MACROS':
        m = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        m.add('🥩 Contar Macros', '💧 Beber Água', '🔥 Calcular TMB', '🛒 Lista de Compras', '🍕 Refeição Livre', '🔙 Voltar')
        bot.send_message(chat_id, "A dieta é 70% do resultado. Escolha:", reply_markup=m)

    elif text == '🤖 PERSONAL IA':
        m = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        m.add('❓ Tirar Dúvida', '🏃 Treino Rápido', '💡 Dica de Postura', '📖 Dicionário Fit', '🔙 Voltar')
        bot.send_message(chat_id, "Sou seu Personal IA. Como posso ajudar?", reply_markup=m)

    elif text == '⚙️ UTILITÁRIOS':
        m = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        m.add('🏆 Ranking', '📸 Foto Progresso', '💰 Mensalidade', '🎶 Playlist', '🔴 Modo Mengão', '🔙 Voltar')
        bot.send_message(chat_id, "Ferramentas extras para você:", reply_markup=m)

    elif text == '🔙 Voltar':
        main_menu(message)
    
    else:
        bot.reply_to(message, f"Você escolheu: {text}. (Função em desenvolvimento para salvar no banco de dados!)")

bot.polling()
