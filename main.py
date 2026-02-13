import os
import telebot
import time
import random
from telebot import types
from flask import Flask
from threading import Thread

# --- SERVIDOR WEB (KEEP ALIVE) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot Academia V12 - GOD MODE (20 Funções)!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- CONFIGURAÇÃO ---
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# ==========================================
# 🧠 DADOS & MEMÓRIA
# ==========================================
user_db = {} # Guarda XP, Peso, Historico, Ofensiva

# TREINOS
treinos = {
    'A': "🔥 **TREINO A (Peito/Tríceps)**\n\n1. [Supino Reto](https://www.youtube.com/results?search_query=execucao+supino+reto) (4x10)\n2. [Supino Inclinado](https://www.youtube.com/results?search_query=execucao+supino+inclinado) (3x12)\n3. [Crucifixo](https://www.youtube.com/results?search_query=execucao+crucifixo+maquina) (3x15)\n4. [Tríceps Corda](https://www.youtube.com/results?search_query=execucao+triceps+corda) (4x12)",
    'B': "🦍 **TREINO B (Costas/Bíceps)**\n\n1. [Puxada Alta](https://www.youtube.com/results?search_query=execucao+puxada+alta) (4x10)\n2. [Remada Curvada](https://www.youtube.com/results?search_query=execucao+remada+curvada) (4x8)\n3. [Rosca Direta](https://www.youtube.com/results?search_query=execucao+rosca+direta) (4x10)\n4. [Rosca Martelo](https://www.youtube.com/results?search_query=execucao+rosca+martelo) (3x12)",
    'C': "🍗 **TREINO C (Pernas)**\n\n1. [Agachamento](https://www.youtube.com/results?search_query=execucao+agachamento) (4x10)\n2. [Leg Press](https://www.youtube.com/results?search_query=execucao+leg+press) (4x12)\n3. [Extensora](https://www.youtube.com/results?search_query=execucao+cadeira+extensora) (3x15)\n4. [Stiff](https://www.youtube.com/results?search_query=execucao+stiff) (4x12)"
}

# PRE-TREINOS
pre_treinos = [
    "🍌 **Leve:** Banana com Aveia e Mel.",
    "☕ **Estimulante:** Café Preto + 3g Creatina.",
    "🥪 **Sólido:** Pão integral com Ovos mexidos.",
    "🥣 **Power:** Iogurte com Granola e Whey."
]

# NIVEIS
niveis = {0: "🐔 Frango", 100: "🏃 Em Obras", 300: "💪 Atlético", 600: "🦍 Monstro", 1000: "👑 Mr. Olympia"}

# ==========================================
# 🤖 MENUS
# ==========================================

@bot.message_handler(commands=['start', 'menu'])
def main_menu(message):
    uid = message.from_user.id
    if uid not in user_db: user_db[uid] = {'xp': 0, 'streak': 0, 'diario': []}
    
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        types.KeyboardButton('🏋️ TREINO & FOCO'),
        types.KeyboardButton('🧰 TÉCNICA & CALC'),
        types.KeyboardButton('🍎 NUTRIÇÃO PRO'),
        types.KeyboardButton('🎮 PERFIL & EXTRAS')
    )
    bot.send_message(message.chat.id, "🔥 **ACADEMIA V12** 🔥\n20 Funções Ativas. Escolha:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def bot_message(message):
    text = message.text
    chat_id = message.chat.id
    uid = message.from_user.id

    # ==========================================
    # 🏋️ MENU 1: TREINO
    # ==========================================
    if text == '🏋️ TREINO & FOCO':
        m = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        m.add('Treino A', 'Treino B', 'Treino C', '🧘 Mobilidade', '🔄 Máquina Ocupada', '🏃 Decisão Cardio', '🔙 Voltar')
        bot.send_message(chat_id, "Bora treinar!", reply_markup=m)

    elif text in ['Treino A', 'Treino B', 'Treino C']:
        tipo = text.split()[-1]
        user_db[uid]['xp'] += 10 # Função 16 (XP)
        bot.send_message(chat_id, f"🆙 **+10 XP!**\n\n{treinos[tipo]}", parse_mode="Markdown", disable_web_page_preview=True)

    elif text == '🧘 Mobilidade': # Função 2
        bot.send_message(chat_id, "🧘 **Antes de começar:**\n[Alongamento Superior](https://www.youtube.com/results?search_query=alongamento+superior)\n[Mobilidade Quadril](https://www.youtube.com/results?search_query=mobilidade+quadril)", parse_mode="Markdown")

    elif text == '🔄 Máquina Ocupada': # Função 4
        bot.send_message(chat_id, "🚫 **Substitutos Rápidos:**\n- Supino ➡️ Flexão ou Halteres\n- Puxada ➡️ Graviton ou Remada\n- Leg Press ➡️ Agachamento Sumô")

    elif text == '🏃 Decisão Cardio': # Função 5
        m = types.InlineKeyboardMarkup()
        m.add(types.InlineKeyboardButton("☔ Está Chovendo", callback_data="chuva"), types.InlineKeyboardButton("☀️ Tem Sol", callback_data="sol"))
        bot.send_message(chat_id, "Como está o tempo aí fora?", reply_markup=m)

    # ==========================================
    # 🧰 MENU 2: TÉCNICA
    # ==========================================
    elif text == '🧰 TÉCNICA & CALC':
        m = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        m.add('⏱️ Timer 60s', '🔥 Tabata', '🧱 Calc. Anilhas', '💪 Calc. 1RM', '📝 Diário', '🆘 Dor ou Lesão', '🔙 Voltar')
        bot.send_message(chat_id, "Ferramentas:", reply_markup=m)

    elif text == '⏱️ Timer 60s': # Função 10
        bot.send_message(chat_id, "⏳ 60 segundos valendo...")
        Thread(target=timer_thread, args=(chat_id, 60, "ACABOU O DESCANSO!")).start()

    elif text == '🔥 Tabata': # Função 3
        bot.send_message(chat_id, "🔥 **TABATA INICIADO!**\nPrepare-se para 4 minutos de inferno.\n(Eu avisarei os ciclos)")
        Thread(target=tabata_thread, args=(chat_id,)).start()

    elif text == '🧱 Calc. Anilhas': # Função 7
        msg = bot.send_message(chat_id, "Quanto peso total na barra (kg)? (Ex: 60)")
        bot.register_next_step_handler(msg, calc_anilhas)

    elif text == '💪 Calc. 1RM': # Função 6
        msg = bot.send_message(chat_id, "Digite: Peso e Repetições (Ex: 40 10)")
        bot.register_next_step_handler(msg, calc_1rm)

    elif text == '📝 Diário': # Função 8
        msg = bot.send_message(chat_id, "O que você pegou hoje? (Ex: Supino 30kg)")
        bot.register_next_step_handler(msg, salvar_diario)

    elif text == '🆘 Dor ou Lesão': # Função 9
        bot.send_message(chat_id, "🏥 **Guia Rápido:**\n- **Dor Muscular:** Aparece 24h depois, dói ao alongar. (É BOM)\n- **Dor Articular:** Pontada aguda, dói parado. (É RUIM, pare!)")

    # ==========================================
    # 🍎 MENU 3: NUTRIÇÃO
    # ==========================================
    elif text == '🍎 NUTRIÇÃO PRO':
        m = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        m.add('💧 Meta Água', '💊 Dose Creatina', '🥩 Meta Proteína', '🍳 Pré-Treino', '💰 Custo Whey', '🔙 Voltar')
        bot.send_message(chat_id, "Dieta:", reply_markup=m)

    elif text == '💧 Meta Água': # Função 11
        msg = bot.send_message(chat_id, "Seu peso (kg)?")
        bot.register_next_step_handler(msg, lambda m: bot.reply_to(m, f"💧 Beba **{float(m.text)*0.035:.2f} Litros** hoje."))

    elif text == '💊 Dose Creatina': # Função 12
        msg = bot.send_message(chat_id, "Seu peso (kg)?")
        bot.register_next_step_handler(msg, lambda m: bot.reply_to(m, f"💊 Tome **{float(m.text)*0.07:.1f}g** de creatina."))
    
    elif text == '🥩 Meta Proteína': # Função 13
        msg = bot.send_message(chat_id, "Seu peso (kg)?")
        bot.register_next_step_handler(msg, lambda m: bot.reply_to(m, f"🥩 Para crescer: **{float(m.text)*2.0:.0f}g** de proteína/dia."))

    elif text == '🍳 Pré-Treino': # Função 14
        bot.send_message(chat_id, f"🎲 Sugestão: {random.choice(pre_treinos)}")

    elif text == '💰 Custo Whey': # Função 15
        msg = bot.send_message(chat_id, "Digite: Preço e Doses do pote (Ex: 150 30)")
        bot.register_next_step_handler(msg, calc_custo)

    # ==========================================
    # 🎮 MENU 4: EXTRAS
    # ==========================================
    elif text == '🎮 PERFIL & EXTRAS':
        m = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        m.add('🏆 Meu Nível', '✅ Check-in', '🔴 MODO MENGÃO', '🎧 DJ Playlist', '🎲 Desafio', '🔙 Voltar')
        bot.send_message(chat_id, "Extras:", reply_markup=m)

    elif text == '🏆 Meu Nível': # Função 16
        xp = user_db[uid]['xp']
        bot.send_message(chat_id, f"🏅 **Seu XP:** {xp}\nPatente: {next((v for k,v in reversed(niveis.items()) if xp>=k), 'Frango')}")

    elif text == '✅ Check-in': # Função 17
        user_db[uid]['streak'] += 1
        bot.send_message(chat_id, f"🔥 **Check-in realizado!**\nOfensiva: {user_db[uid]['streak']} dias seguidos.")

    elif text == '🔴 MODO MENGÃO': # Função 18
        bot.send_message(chat_id, "🔴⚫ **VAMOS FLAMENGO!**\nLevanta esse peso com RAÇA!\n🎶 *Uma vez Flamengo...*")

    elif text == '🎲 Desafio': # Função 19
        bot.send_message(chat_id, f"🎲 **DESAFIO AGORA:** {random.choice(['20 Flexões', '1min Prancha', '50 Polichinelos'])}!")
    
    elif text == '🎧 DJ Playlist': # Função 20
        bot.send_message(chat_id, "🎧 **Playlists:**\n[Rock Treino](https://open.spotify.com/playlist/37i9dQZF1DWXRqgorJj26U) | [Funk](https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd)", parse_mode="Markdown")

    elif text == '🔙 Voltar':
        main_menu(message)

# ==========================================
# 📐 FUNÇÕES MATEMÁTICAS E LÓGICA
# ==========================================

def calc_anilhas(message):
    try:
        total = float(message.text)
        lado = (total - 20) / 2 # Tira barra de 20kg
        if lado < 0:
            bot.reply_to(message, "A barra sozinha já pesa 20kg!")
        else:
            bot.reply_to(message, f"🧱 **Montagem:**\nColoque **{lado}kg** de CADA lado da barra.")
    except:
        bot.reply_to(message, "Erro. Use apenas números.")

def calc_1rm(message):
    try:
        peso, reps = map(int, message.text.split())
        rm = peso * (1 + (reps/30))
        bot.reply_to(message, f"💪 Sua Força Máxima (1RM): **{rm:.1f}kg**")
    except:
        bot.reply_to(message, "Use formato: 40 10")

def calc_custo(message):
    try:
        preco, doses = map(float, message.text.split())
        bot.reply_to(message, f"💰 Custo por treino: **R$ {preco/doses:.2f}**")
    except:
        bot.reply_to(message, "Erro.")

def salvar_diario(message):
    user_db[message.from_user.id]['diario'].append(message.text)
    bot.reply_to(message, "✅ Salvo no diário!")

# --- THREADS (TIMERS) ---
def timer_thread(chat_id, tempo, msg):
    time.sleep(tempo)
    bot.send_message(chat_id, f"⏰ {msg}")

def tabata_thread(chat_id):
    # Simula um ciclo curto de Tabata (Exemplo)
    bot.send_message(chat_id, "🟢 **GO! (20s)**")
    time.sleep(20)
    bot.send_message(chat_id, "🔴 **DESCANSAR (10s)**")
    time.sleep(10)
    bot.send_message(chat_id, "🟢 **GO! (20s)**")
    time.sleep(20)
    bot.send_message(chat_id, "🏁 **TABATA FINALIZADO!**")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "chuva":
        bot.send_message(call.message.chat.id, "☔ Chuva? **Esteira ou Escada** na academia!")
    elif call.data == "sol":
        bot.send_message(call.message.chat.id, "☀️ Sol? **Corrida na Rua ou Bike**!")

# --- START ---
keep_alive()
try:
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
except Exception:
    pass
