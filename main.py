import os
import telebot
import time
import random
import requests
import base64
from telebot import types
from flask import Flask
from threading import Thread

# --- SERVIDOR WEB (KEEP ALIVE) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot V19 - O MEGAZORD COM IA CORRIGIDA!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- CONFIGURAÇÃO BOT ---
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# ==========================================
# 🧠 BANCO DE DADOS E CONTEÚDO
# ==========================================
user_db = {} 

# TREINOS ACADEMIA
treinos_gym = {
    'Treino A': "🔥 **TREINO A (Peito/Tríceps)**\n\n1. [Supino Reto](https://www.youtube.com/results?search_query=execucao+supino+reto) (4x10)\n2. [Supino Inclinado](https://www.youtube.com/results?search_query=execucao+supino+inclinado) (3x12)\n3. [Crucifixo](https://www.youtube.com/results?search_query=execucao+crucifixo+maquina) (3x15)\n4. [Tríceps Corda](https://www.youtube.com/results?search_query=execucao+triceps+corda) (4x12)",
    'Treino B': "🦍 **TREINO B (Costas/Bíceps)**\n\n1. [Puxada Alta](https://www.youtube.com/results?search_query=execucao+puxada+alta) (4x10)\n2. [Remada Curvada](https://www.youtube.com/results?search_query=execucao+remada+curvada) (4x8)\n3. [Rosca Direta](https://www.youtube.com/results?search_query=execucao+rosca+direta) (4x10)\n4. [Rosca Martelo](https://www.youtube.com/results?search_query=execucao+rosca+martelo) (3x12)",
    'Treino C': "🍗 **TREINO C (Pernas)**\n\n1. [Agachamento](https://www.youtube.com/results?search_query=execucao+agachamento) (4x10)\n2. [Leg Press](https://www.youtube.com/results?search_query=execucao+leg+press) (4x12)\n3. [Extensora](https://www.youtube.com/results?search_query=execucao+cadeira+extensora) (3x15)\n4. [Stiff](https://www.youtube.com/results?search_query=execucao+stiff) (4x12)"
}

# TREINOS EM CASA
treinos_casa = {
    '🏠 FullBody Casa': "🏠 **TREINO EM CASA (Corpo Todo)**\n\n1. [Polichinelos](https://www.youtube.com/results?search_query=polichinelos) (3x50)\n2. [Flexão](https://www.youtube.com/results?search_query=flexao+de+braco) (4xFalha)\n3. [Agachamento](https://www.youtube.com/results?search_query=agachamento+livre) (4x20)\n4. [Abdominal](https://www.youtube.com/results?search_query=abdominal+remador) (3x20)\n5. [Prancha](https://www.youtube.com/results?search_query=prancha+abdominal) (3x 1min)",
    '🏠 HIIT Casa': "🔥 **HIIT EM CASA (Queima Gordura)**\n\n1. [Burpees](https://www.youtube.com/results?search_query=burpees) (3x10)\n2. [Corrida no Lugar](https://www.youtube.com/results?search_query=corrida+estacionaria) (3x1min)\n3. [Mountain Climber](https://www.youtube.com/results?search_query=mountain+climber) (3x30s)\n4. [Agachamento com Salto](https://www.youtube.com/results?search_query=agachamento+com+salto) (3x15)"
}

pre_treinos = ["🍌 Banana + Aveia e Mel", "☕ Café Preto + 3g Creatina", "🥪 Pão com Ovo Mexido", "🥣 Iogurte + Granola e Whey"]
niveis = {0: "🐔 Frango", 100: "🏃 Em Obras", 300: "💪 Atlético", 600: "🦍 Monstro", 1000: "👑 Mr. Olympia"}
desafios = ["20 Flexões AGORA!", "1min de Prancha!", "50 Polichinelos!", "Ficar agachado na parede 1min!"]

# ==========================================
# 🤖 MENUS
# ==========================================

@bot.message_handler(commands=['start', 'menu'])
def main_menu(message):
    uid = message.from_user.id
    if uid not in user_db: user_db[uid] = {'xp': 0, 'streak': 0, 'diario': []}
    
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        types.KeyboardButton('🏋️ TREINOS (GYM & CASA)'),
        types.KeyboardButton('📸 NUTRIÇÃO & IA'),
        types.KeyboardButton('🛠️ FERRAMENTAS'),
        types.KeyboardButton('🎮 PERFIL & EXTRAS')
    )
    bot.send_message(message.chat.id, "🔥 **SISTEMA V19 - MEGAZORD ATIVO** 🔥\nEscolha sua missão:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def bot_message(message):
    text = message.text
    chat_id = message.chat.id
    uid = message.from_user.id

    # === 1. TREINOS ===
    if text == '🏋️ TREINOS (GYM & CASA)':
        m = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        m.add('Treino A', 'Treino B', 'Treino C', '🏠 FullBody Casa', '🏠 HIIT Casa', '🧘 Mobilidade', '🔄 Máquina Ocupada', '🔙 Voltar')
        bot.send_message(chat_id, "Bora treinar! Onde vai ser?", reply_markup=m)

    elif text in treinos_gym:
        user_db[uid]['xp'] += 10
        bot.send_message(chat_id, f"🆙 **+10 XP!**\n\n{treinos_gym[text]}", parse_mode="Markdown", disable_web_page_preview=True)

    elif text in treinos_casa:
        user_db[uid]['xp'] += 15
        bot.send_message(chat_id, f"🆙 **+15 XP!** (Guerreiro!)\n\n{treinos_casa[text]}", parse_mode="Markdown", disable_web_page_preview=True)

    elif text == '🧘 Mobilidade':
        bot.send_message(chat_id, "🧘 **Mobilidade Rápida:**\n[Alongamento 5min](https://www.youtube.com/results?search_query=alongamento+antes+treino)", parse_mode="Markdown", disable_web_page_preview=True)

    elif text == '🔄 Máquina Ocupada':
        bot.send_message(chat_id, "🚫 **Alternativas:**\nSupino ➡️ Flexão ou Halteres\nPuxada ➡️ Graviton ou Remada Livre\nLeg Press ➡️ Agachamento Sumô")

    # === 2. NUTRIÇÃO & IA ===
    elif text == '📸 NUTRIÇÃO & IA':
        m = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        m.add('📷 Analisar Prato (IA)', '💧 Meta Água', '💊 Creatina', '🥩 Proteína', '🍳 Pré-Treino', '🔙 Voltar')
        bot.send_message(chat_id, "Nutrição Inteligente:", reply_markup=m)

    elif text == '📷 Analisar Prato (IA)':
        bot.send_message(chat_id, "🍽️ **Envie uma FOTO da sua comida agora!**\nA Inteligência Artificial vai analisar os alimentos para você.")

    elif text == '💧 Meta Água':
        msg = bot.send_message(chat_id, "Qual o seu peso (kg)?")
        bot.register_next_step_handler(msg, lambda m: bot.reply_to(m, f"💧 Meta: **{float(m.text.replace(',','.'))*0.035:.2f} L** de água."))

    elif text == '💊 Creatina':
        msg = bot.send_message(chat_id, "Qual o seu peso (kg)?")
        bot.register_next_step_handler(msg, lambda m: bot.reply_to(m, f"💊 Dose: **{float(m.text.replace(',','.'))*0.07:.1f}g**"))
    
    elif text == '🥩 Proteína':
        msg = bot.send_message(chat_id, "Qual o seu peso (kg)?")
        bot.register_next_step_handler(msg, lambda m: bot.reply_to(m, f"🥩 Hipertrofia: **{float(m.text.replace(',','.'))*2.0:.0f}g** de proteína/dia."))

    elif text == '🍳 Pré-Treino':
        bot.send_message(chat_id, f"🎲 Sugestão: **{random.choice(pre_treinos)}**")

    # === 3. FERRAMENTAS ===
    elif text == '🛠️ FERRAMENTAS':
        m = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        m.add('⏱️ Timer 60s', '🔥 Tabata', '🧱 Calc. Anilhas', '💪 Calc. 1RM', '📝 Diário', '🆘 Dor vs Lesão', '🔙 Voltar')
        bot.send_message(chat_id, "Caixa de Ferramentas:", reply_markup=m)

    elif text == '⏱️ Timer 60s':
        bot.send_message(chat_id, "⏳ 60s valendo. Respire...")
        Thread(target=timer_thread, args=(chat_id,)).start()

    elif text == '🔥 Tabata':
        bot.send_message(chat_id, "🔥 **TABATA INICIADO!** (20s fazendo / 10s descansando).")
        Thread(target=tabata_thread, args=(chat_id,)).start()

    elif text == '🧱 Calc. Anilhas':
        msg = bot.send_message(chat_id, "Qual o peso TOTAL na barra (kg)?")
        bot.register_next_step_handler(msg, calc_anilhas)

    elif text == '💪 Calc. 1RM':
        msg = bot.send_message(chat_id, "Digite: Peso e Repetições (Ex: 40 10)")
        bot.register_next_step_handler(msg, calc_1rm)

    elif text == '📝 Diário':
        msg = bot.send_message(chat_id, "O que quer anotar? (Ex: Supino 30kg)")
        bot.register_next_step_handler(msg, lambda m: bot.reply_to(m, "✅ Salvo no diário!"))

    elif text == '🆘 Dor vs Lesão':
        bot.send_message(chat_id, "🏥 **Muscular:** Dói no dia seguinte (Normal).\n**Lesão:** Pontada aguda, estalos (PARE!).")

    # === 4. EXTRAS ===
    elif text == '🎮 PERFIL & EXTRAS':
        m = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        m.add('🏆 Meu Nível', '✅ Check-in', '🔴 MODO MENGÃO', '🎧 DJ Playlist', '🎲 Desafio', '🔙 Voltar')
        bot.send_message(chat_id, "Área Gamer e Diversão:", reply_markup=m)

    elif text == '🏆 Meu Nível':
        xp = user_db[uid]['xp']
        patente = next((v for k,v in reversed(niveis.items()) if xp>=k), 'Frango')
        bot.send_message(chat_id, f"🏅 **XP:** {xp}\n🏷️ **Patente:** {patente}")

    elif text == '✅ Check-in':
        user_db[uid]['streak'] += 1
        bot.send_message(chat_id, f"🔥 **Check-in!** Ofensiva: {user_db[uid]['streak']} dias seguidos.")

    elif text == '🔴 MODO MENGÃO':
        bot.send_message(chat_id, "🔴⚫ **VAMOS FLAMENGO!** Raça, amor e paixão! 💪🦅")

    elif text == '🎲 Desafio':
        bot.send_message(chat_id, f"🎲 **DESAFIO:** {random.choice(desafios)}")

    elif text == '🎧 DJ Playlist':
        bot.send_message(chat_id, "🎧 **Spotify Workout:**\n[Playlist Treino Pesado](https://open.spotify.com/playlist/37i9dQZF1DWXRqgorJj26U)")

    elif text == '🔙 Voltar':
        main_menu(message)

# ==========================================
# 📸 A MÁGICA DIRETA (API GEMINI CORRIGIDA)
# ==========================================
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    GEMINI_KEY = os.getenv('GEMINI_KEY')
    if not GEMINI_KEY:
        bot.reply_to(message, "⚠️ Chave GEMINI_KEY não encontrada no Render.")
        return
    
    bot.reply_to(message, "🤖 **Lendo a imagem com a IA do Google...**")
    try:
        # 1. Baixa a foto do Telegram
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # 2. Converte a foto para Base64
        img_b64 = base64.b64encode(downloaded_file).decode('utf-8')
        
        # 3. Monta o pacote EXATAMENTE como o Google exige (inlineData e mimeType sem underline)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
        payload = {
            "contents": [{
                "parts": [
                    {"text": "Analise esta foto de refeição. Diga os alimentos que você consegue identificar, faça uma estimativa das calorias totais e dos macronutrientes (Proteína, Carboidrato e Gordura). Responda em Português do Brasil de forma amigável."},
                    {"inlineData": {"mimeType": "image/jpeg", "data": img_b64}}
                ]
            }]
        }
        headers = {'Content-Type': 'application/json'}
        
        # 4. Dispara a requisição
        response = requests.post(url, json=payload, headers=headers)
        
        # 5. Lê a resposta
        if response.status_code == 200:
            dados = response.json()
            texto_ia = dados['candidates'][0]['content']['parts'][0]['text']
            bot.reply_to(message, f"🍽️ **ANÁLISE NUTRICIONAL:**\n\n{texto_ia}", parse_mode="Markdown")
        else:
            # Se der erro, ele conta exatamente o que houve
            erro_real = response.json().get('error', {}).get('message', 'Erro desconhecido')
            bot.reply_to(message, f"❌ O Google recusou. Motivo exato: {erro_real}")
            
    except Exception as e:
        bot.reply_to(message, f"❌ Erro interno: {e}")

# ==========================================
# 📐 CÁLCULOS
# ==========================================
def calc_anilhas(message):
    try:
        total = float(message.text.replace(',', '.'))
        lado = (total - 20) / 2 
        if lado <= 0: bot.reply_to(message, "A barra já pesa 20kg!")
        else: bot.reply_to(message, f"🧱 Coloque **{lado}kg** de CADA lado.")
    except: bot.reply_to(message, "❌ Apenas números.")

def calc_1rm(message):
    try:
        peso, reps = map(float, message.text.replace(',', '.').split())
        rm = peso * (1 + (reps/30))
        bot.reply_to(message, f"💪 **1RM:** Você aguenta **{rm:.1f}kg** para 1 rep.")
    except: bot.reply_to(message, "❌ Digite: 40 10")

# ==========================================
# ⏱️ TIMERS
# ==========================================
def timer_thread(chat_id):
    time.sleep(60)
    bot.send_message(chat_id, "⏰ **ACABOU O DESCANSO!**")

def tabata_thread(chat_id):
    bot.send_message(chat_id, "🟢 **GO! (20s)**")
    time.sleep(20)
    bot.send_message(chat_id, "🔴 **PAUSA! (10s)**")
    time.sleep(10)
    bot.send_message(chat_id, "🟢 **GO! (20s)**")
    time.sleep(20)
    bot.send_message(chat_id, "🏁 **FIM DO CICLO!**")

# --- START ---
keep_alive()
try:
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
except Exception:
    pass
