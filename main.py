import os
import telebot
import time
from telebot import types
from flask import Flask
from threading import Thread

# --- SERVIDOR WEB (PARA O RENDER NÃO DORMIR) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot Academia V3 - Com GIFs e Música!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- CONFIGURAÇÃO ---
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# --- LINKS DE GIFS (AQUI ESTÁ A MÁGICA VISUAL) ---
gifs = {
    'supino': 'https://media.tenor.com/J1D9yJ6F1O4AAAAC/bench-press-chest.gif',
    'puxada': 'https://media.tenor.com/NbC0ePqF4wEAAAAC/lat-pulldown-workout.gif',
    'legpress': 'https://media.tenor.com/G5g2B2vM3hIAAAAC/leg-press-workout.gif',
    'agachamento': 'https://media.tenor.com/Post4Ww_HwUAAAAC/squat-exercise.gif'
}

# --- TIMER ---
def contar_tempo(chat_id):
    time.sleep(60)
    bot.send_message(chat_id, "⏰ ACABOU O DESCANSO! Bora pra próxima série! 💪")

# --- MENU PRINCIPAL ---
@bot.message_handler(commands=['start', 'menu'])
def main_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        types.KeyboardButton('🏋️ ÁREA DE TREINO'),
        types.KeyboardButton('🍎 DIETA E MACROS'),
        types.KeyboardButton('🤖 PERSONAL IA'),
        types.KeyboardButton('⚙️ UTILITÁRIOS')
    )
    bot.send_message(message.chat.id, "Fala David! O que vamos fazer agora?", reply_markup=markup)

# --- RESPOSTAS ---
@bot.message_handler(func=lambda message: True)
def bot_message(message):
    text = message.text
    chat_id = message.chat.id

    # === 1. ÁREA DE TREINO ===
    if text == '🏋️ ÁREA DE TREINO':
        m = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        m.add('📅 Treino A (Peito)', '📅 Treino B (Costas)', '📅 Treino C (Pernas)', '⏱️ Timer 60s', '🔙 Voltar')
        bot.send_message(chat_id, "Escolha seu treino de hoje:", reply_markup=m)

    # --- TREINO A (COM BOTÃO DE VISUALIZAR) ---
    elif text == '📅 Treino A (Peito)':
        treino = (
            "🏋️ **TREINO A - PEITO E TRÍCEPS**\n\n"
            "1. Supino Reto (4x 10)\n"
            "2. Supino Inclinado (3x 12)\n"
            "3. Tríceps Corda (4x 12)"
        )
        # Botão Inline (Aparece embaixo da mensagem)
        markup = types.InlineKeyboardMarkup()
        btn_ver = types.InlineKeyboardButton("🎥 Ver Execução do Supino", callback_data="ver_supino")
        markup.add(btn_ver)
        bot.send_message(chat_id, treino, parse_mode="Markdown", reply_markup=markup)

    # --- TREINO B ---
    elif text == '📅 Treino B (Costas)':
        treino = (
            "🦍 **TREINO B - COSTAS E BÍCEPS**\n\n"
            "1. Puxada Alta (4x 12)\n"
            "2. Remada Curvada (4x 10)\n"
            "3. Rosca Direta (4x 12)"
        )
        markup = types.InlineKeyboardMarkup()
        btn_ver = types.InlineKeyboardButton("🎥 Ver Execução da Puxada", callback_data="ver_puxada")
        markup.add(btn_ver)
        bot.send_message(chat_id, treino, parse_mode="Markdown", reply_markup=markup)

    # --- TREINO C ---
    elif text == '📅 Treino C (Pernas)':
        treino = (
            "🍗 **TREINO C - PERNAS**\n\n"
            "1. Agachamento Livre (4x 10)\n"
            "2. Leg Press 45 (4x 12)\n"
            "3. Cadeira Extensora (3x 15)"
        )
        markup = types.InlineKeyboardMarkup()
        btn_ver1 = types.InlineKeyboardButton("🎥 Ver Agachamento", callback_data="ver_agachamento")
        btn_ver2 = types.InlineKeyboardButton("🎥 Ver Leg Press", callback_data="ver_legpress")
        markup.add(btn_ver1, btn_ver2)
        bot.send_message(chat_id, treino, parse_mode="Markdown", reply_markup=markup)

    elif text == '⏱️ Timer 60s':
        bot.send_message(chat_id, "⏳ Contando 60 segundos...")
        Thread(target=contar_tempo, args=(chat_id,)).start()

    # === 2. UTILITÁRIOS (COM A PLAYLIST) ===
    elif text == '⚙️ UTILITÁRIOS':
        m = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        m.add('🎶 Playlist de Treino', '💰 Mensalidade', '🔙 Voltar')
        bot.send_message(chat_id, "Utilitários:", reply_markup=m)

    elif text == '🎶 Playlist de Treino':
        bot.send_message(chat_id, "🎧 **Solta o som!** Aqui está uma playlist pra dar gás:\n\n👉 https://open.spotify.com/playlist/37i9dQZF1DX76Wlfdnj7AP")

    elif text == '🔙 Voltar':
        main_menu(message)

    else:
        bot.send_message(chat_id, "Use os botões! 💪")

# --- HANDLER DOS BOTÕES DE VÍDEO (CALLBACKS) ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    # O bot responde com o GIF correspondente
    if call.data == "ver_supino":
        bot.send_video(call.message.chat.id, gifs['supino'], caption="💡 **Dica:** Desça a barra até o peito devagar e suba explosivo.")
    elif call.data == "ver_puxada":
        bot.send_video(call.message.chat.id, gifs['puxada'], caption="💡 **Dica:** Puxe com os cotovelos, não com as mãos!")
    elif call.data == "ver_legpress":
        bot.send_video(call.message.chat.id, gifs['legpress'], caption="💡 **Dica:** Não estenda o joelho todo na volta, mantenha flexionado.")
    elif call.data == "ver_agachamento":
        bot.send_video(call.message.chat.id, gifs['agachamento'], caption="💡 **Dica:** Mantenha a coluna reta e desça como se fosse sentar.")

# --- INICIAR ---
keep_alive()
bot.infinity_polling()
