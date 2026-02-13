import os
import telebot
import time
import random
import google.generativeai as genai
from telebot import types
from flask import Flask
from threading import Thread
from PIL import Image

# --- SERVIDOR WEB ---
app = Flask('')

@app.route('/')
def home():
    return "Bot Academia V13 - COM VISÃO IA!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- CONFIGURAÇÃO ---
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# CONFIGURAÇÃO DA IA (GEMINI)
GEMINI_KEY = os.getenv('GEMINI_KEY')
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash') # Modelo rápido e grátis
else:
    model = None

# ==========================================
# 🧠 DADOS (TREINOS)
# ==========================================
user_db = {} 

# TREINOS DE ACADEMIA
treinos_gym = {
    'A': "🔥 **TREINO GYM A (Peito/Tríceps)**\n\n1. [Supino Reto](https://www.youtube.com/results?search_query=execucao+supino+reto) (4x10)\n2. [Supino Inclinado](https://www.youtube.com/results?search_query=execucao+supino+inclinado) (3x12)\n3. [Tríceps Corda](https://www.youtube.com/results?search_query=execucao+triceps+corda) (4x12)",
    'B': "🦍 **TREINO GYM B (Costas/Bíceps)**\n\n1. [Puxada Alta](https://www.youtube.com/results?search_query=execucao+puxada+alta) (4x10)\n2. [Remada Curvada](https://www.youtube.com/results?search_query=execucao+remada+curvada) (4x10)\n3. [Rosca Direta](https://www.youtube.com/results?search_query=execucao+rosca+direta) (4x10)",
    'C': "🍗 **TREINO GYM C (Pernas)**\n\n1. [Agachamento](https://www.youtube.com/results?search_query=execucao+agachamento) (4x10)\n2. [Leg Press](https://www.youtube.com/results?search_query=execucao+leg+press) (4x12)\n3. [Extensora](https://www.youtube.com/results?search_query=execucao+cadeira+extensora) (3x15)"
}

# TREINOS EM CASA (SEM EQUIPAMENTO)
treinos_casa = {
    'FullBody': "🏠 **TREINO EM CASA (Corpo Todo)**\n\n1. [Polichinelos](https://www.youtube.com/results?search_query=polichinelos) (3x 50)\n2. [Flexão de Braço](https://www.youtube.com/results?search_query=flexao+de+braco) (4x Falha)\n3. [Agachamento Livre](https://www.youtube.com/results?search_query=agachamento+livre) (4x 20)\n4. [Abdominal Remador](https://www.youtube.com/results?search_query=abdominal+remador) (3x 20)\n5. [Prancha](https://www.youtube.com/results?search_query=prancha+abdominal) (3x 45seg)",
    'HIIT': "🔥 **TREINO CARDIO EM CASA (Queima Gordura)**\n\n1. [Burpees](https://www.youtube.com/results?search_query=burpees) (3x 10)\n2. [Corrida Estacionária](https://www.youtube.com/results?search_query=corrida+estacionaria) (3x 1min)\n3. [Mountain Climber](https://www.youtube.com/results?search_query=mountain+climber) (3x 30seg)\n4. [Agachamento com Salto](https://www.youtube.com/results?search_query=agachamento+com+salto) (3x 15)"
}

# ==========================================
# 🤖 LÓGICA DO BOT
# ==========================================

@bot.message_handler(commands=['start', 'menu'])
def main_menu(message):
    uid = message.from_user.id
    if uid not in user_db: user_db[uid] = {'xp': 0}
    
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        types.KeyboardButton('🏋️ TREINO ACADEMIA'),
        types.KeyboardButton('🏠 TREINO EM CASA'),
        types.KeyboardButton('📸 CALORIAS POR FOTO'),
        types.KeyboardButton('🎮 EXTRAS & PERFIL')
    )
    bot.send_message(message.chat.id, "🔥 **ACADEMIA V13 - IA ATIVADA** 🔥\nEscolha sua missão:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def bot_text_message(message):
    text = message.text
    chat_id = message.chat.id
    uid = message.from_user.id

    # === TREINO ACADEMIA ===
    if text == '🏋️ TREINO ACADEMIA':
        m = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        m.add('Treino A', 'Treino B', 'Treino C', '🔙 Voltar')
        bot.send_message(chat_id, "Foco na máquina! Qual o treino?", reply_markup=m)

    elif text in treinos_gym:
        user_db[uid]['xp'] += 10
        bot.send_message(chat_id, f"🆙 **+10 XP!**\n\n{treinos_gym[text]}", parse_mode="Markdown", disable_web_page_preview=True)

    # === TREINO EM CASA (NOVO) ===
    elif text == '🏠 TREINO EM CASA':
        m = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        m.add('FullBody', 'HIIT', '🔙 Voltar')
        bot.send_message(chat_id, "🏠 Sem grana? Sem problema! O chão é sua academia.", reply_markup=m)

    elif text in treinos_casa:
        user_db[uid]['xp'] += 15 # Dá mais XP pq treinar em casa exige disciplina!
        bot.send_message(chat_id, f"🆙 **+15 XP!** (Guerreiro!)\n\n{treinos_casa[text]}", parse_mode="Markdown", disable_web_page_preview=True)

    # === NUTRIÇÃO IA ===
    elif text == '📸 CALORIAS POR FOTO':
        if not model:
            bot.send_message(chat_id, "⚠️ **ERRO:** A chave da IA não foi configurada no Render.")
        else:
            bot.send_message(chat_id, "🍽️ **Mande uma FOTO do seu prato agora!**\n\nA Inteligência Artificial vai analisar os ingredientes e estimar as calorias.")

    # === EXTRAS ===
    elif text == '🎮 EXTRAS & PERFIL':
        xp = user_db[uid]['xp']
        bot.send_message(chat_id, f"🏆 **SEU PERFIL:**\nXP Total: {xp}\n\n(Menu simplificado para focar na IA)")

    elif text == '🔙 Voltar':
        main_menu(message)

# ==========================================
# 📸 A MÁGICA DA IA (RECEBER FOTO)
# ==========================================
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if not model:
        bot.reply_to(message, "IA não configurada.")
        return

    bot.reply_to(message, "🤖 **Analisando sua comida...** (Aguarde uns segundos)")

    try:
        # 1. Baixar a foto que o usuário mandou
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # 2. Salvar temporariamente
        temp_filename = "food.jpg"
        with open(temp_filename, 'wb') as new_file:
            new_file.write(downloaded_file)

        # 3. Preparar imagem para o Gemini
        img = Image.open(temp_filename)

        # 4. Enviar para a IA
        prompt = "Analise esta imagem de comida. Liste os alimentos visíveis e faça uma estimativa aproximada das calorias totais e macronutrientes (Proteína, Carbo, Gordura). Seja direto e resumido. Fale em Português."
        response = model.generate_content([prompt, img])

        # 5. Responder ao usuário
        bot.reply_to(message, f"🍽️ **ANÁLISE DO PRATO:**\n\n{response.text}\n\n⚠️ _Estimativa via IA. Pode haver variações._", parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"Deu erro na análise: {e}")

# --- START ---
keep_alive()
try:
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
except Exception:
    pass
