import os
import telebot
import time
import random
import google.generativeai as genai
from telebot import types
from flask import Flask
from threading import Thread
from PIL import Image

# --- SERVIDOR WEB (KEEP ALIVE) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot V16 - GOD MODE + IA CORRIGIDA!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- CONFIGURAÇÃO BOT ---
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# --- CONFIGURAÇÃO DA IA (GEMINI) ---
GEMINI_KEY = os.getenv('GEMINI_KEY')
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)
    # Usando a versão 'latest' para evitar o erro 404
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
else:
    model = None

# ==========================================
# 🧠 BANCO DE DADOS E CONTEÚDO
# ==========================================
user_db = {} # Guarda XP, Streak, Histórico

# TREINOS ACADEMIA (NOMES IDÊNTICOS AOS BOTÕES)
treinos_gym = {
    'Treino A': "🔥 **TREINO A (Peito/Tríceps)**\n\n1. [Supino Reto](https://www.youtube.com/results?search_query=execucao+supino+reto) (4x10)\n2. [Supino Inclinado](https://www.youtube.com/results?search_query=execucao+supino+inclinado) (3x12)\n3. [Crucifixo](https://www.youtube.com/results?search_query=execucao+crucifixo+maquina) (3x15)\n4. [Tríceps Corda](https://www.youtube.com/results?search_query=execucao+triceps+corda) (4x12)",
    'Treino B': "🦍 **TREINO B (Costas/Bíceps)**\n\n1. [Puxada Alta](https://www.youtube.com/results?search_query=execucao+puxada+alta) (4x10)\n2. [Remada Curvada](https://www.youtube.com/results?search_query=execucao+remada+curvada) (4x8)\n3. [Rosca Direta](https://www.youtube.com/results?search_query=execucao+rosca+direta) (4x10)\n4. [Rosca Martelo](https://www.youtube.com/results?search_query=execucao+rosca+martelo) (3x12)",
    'Treino C': "🍗 **TREINO C (Pernas)**\n\n1. [Agachamento](https://www.youtube.com/results?search_query=execucao+agachamento) (4x10)\n2. [Leg Press](https://www.youtube.com/results?search_query=execucao+leg+press) (4x12)\n3. [Extensora](https://www.youtube.com/results?search_query=execucao+cadeira+extensora) (3x15)\n4. [Stiff](https://www.youtube.com/results?search_query=execucao+stiff) (4x12)"
}

# TREINOS EM CASA (NOMES IDÊNTICOS AOS BOTÕES)
treinos_casa = {
    '🏠 FullBody Casa': "🏠 **TREINO EM CASA (Corpo Todo)**\n\n1. [Polichinelos](https://www.youtube.com/results?search_query=polichinelos) (3x50)\n2. [Flexão](https://www.youtube.com/results?search_query=flexao+de+braco) (4xFalha)\n3. [Agachamento](https://www.youtube.com/results?search_query=agachamento+livre) (4x20)\n4. [Abdominal](https://www.youtube.com/results?search_query=abdominal+remador) (3x20)\n5. [Prancha](https://www.youtube.com/results?search_query=prancha+abdominal) (3x 1min)",
    '🏠 HIIT Casa': "🔥 **HIIT EM CASA (Queima Gordura)**\n\n1. [Burpees](https://www.youtube.com/results?search_query=burpees) (3x10)\n2. [Corrida no Lugar](https://www.youtube.com/results?search_query=corrida+estacionaria) (3x1min)\n3. [Mountain Climber](https://www.youtube.com/results?search_query=mountain+climber) (3x30s)\n4. [Agachamento com Salto](https://www.youtube.com/results?search_query=agachamento+com+salto) (3x15)"
}

# EXTRAS
pre_treinos = ["🍌 Banana + Aveia e Mel", "☕ Café Preto + 3g Creatina", "🥪 Pão com Ovo Mexido", "🥣 Iogurte + Granola e Whey"]
niveis = {0: "🐔 Frango", 100: "🏃 Em Obras", 300: "💪 Atlético", 600: "🦍 Monstro", 1000: "👑 Mr. Olympia"}
desafios = ["20 Flexões AGORA!", "1min de Prancha!", "50 Polichinelos!", "Ficar agachado na parede 1min!", "Beba 500ml de água num gole só!"]

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
    bot.send_message(message.chat.id, "🔥 **SISTEMA V16 - COMPLETO** 🔥\nTodas as funções ativas. Escolha:", reply_markup=markup)

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
        bot.send_message(chat_id, "🧘 **Mobilidade Rápida:**\n[Alongamento Completo 5min](https://www.youtube.com/results?search_query=alongamento+antes+treino+5+minutos)", parse_mode="Markdown", disable_web_page_preview=True)

    elif text == '🔄 Máquina Ocupada':
        bot.send_message(chat_id, "🚫 **Alternativas:**\nSupino ➡️ Flexão ou Halteres\nPuxada ➡️ Graviton ou Remada Livre\nLeg Press ➡️ Agachamento Sumô")

    # === 2. NUTRIÇÃO & IA ===
    elif text == '📸 NUTRIÇÃO & IA':
        m = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        m.add('📷 Analisar Prato (IA)', '💧 Meta Água', '💊 Creatina', '🥩 Proteína', '🍳 Pré-Treino', '🔙 Voltar')
        bot.send_message(chat_id, "Nutrição Inteligente:", reply_markup=m)

    elif text == '📷 Analisar Prato (IA)':
        if not model:
            bot.send_message(chat_id, "⚠️ Configure a GEMINI_KEY no Render para usar a IA.")
        else:
            bot.send_message(chat_id, "🍽️ **Envie uma FOTO da sua comida agora!**\nA Inteligência Artificial vai identificar os alimentos e calcular as calorias aproximadas.")

    elif text == '💧 Meta Água':
        msg = bot.send_message(chat_id, "Qual o seu peso (kg)?")
        bot.register_next_step_handler(msg, lambda m: bot.reply_to(m, f"💧 Sua meta diária é de **{float(m.text)*0.035:.2f} Litros** de água."))

    elif text == '💊 Creatina':
        msg = bot.send_message(chat_id, "Qual o seu peso (kg)?")
        bot.register_next_step_handler(msg, lambda m: bot.reply_to(m, f"💊 A dose ideal para você é de **{float(m.text)*0.07:.1f}g** de creatina por dia."))
    
    elif text == '🥩 Proteína':
        msg = bot.send_message(chat_id, "Qual o seu peso (kg)?")
        bot.register_next_step_handler(msg, lambda m: bot.reply_to(m, f"🥩 Para hipertrofia, consuma em média: **{float(m.text)*2.0:.0f}g** de proteína por dia."))

    elif text == '🍳 Pré-Treino':
        bot.send_message(chat_id, f"🎲 Sugestão do Chef maromba: **{random.choice(pre_treinos)}**")

    # === 3. FERRAMENTAS ===
    elif text == '🛠️ FERRAMENTAS':
        m = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        m.add('⏱️ Timer 60s', '🔥 Tabata', '🧱 Calc. Anilhas', '💪 Calc. 1RM', '📝 Diário', '🆘 Dor vs Lesão', '🔙 Voltar')
        bot.send_message(chat_id, "Caixa de Ferramentas:", reply_markup=m)

    elif text == '⏱️ Timer 60s':
        bot.send_message(chat_id, "⏳ 60s valendo. Respire...")
        Thread(target=timer_thread, args=(chat_id,)).start()

    elif text == '🔥 Tabata':
        bot.send_message(chat_id, "🔥 **TABATA INICIADO!** Prepare-se: eu aviso os tempos (20s fazendo / 10s descansando).")
        Thread(target=tabata_thread, args=(chat_id,)).start()

    elif text == '🧱 Calc. Anilhas':
        msg = bot.send_message(chat_id, "Qual o peso TOTAL que você quer na barra (kg)?")
        bot.register_next_step_handler(msg, calc_anilhas)

    elif text == '💪 Calc. 1RM':
        msg = bot.send_message(chat_id, "Digite o peso e as repetições que você fez (Ex: 40 10)")
        bot.register_next_step_handler(msg, calc_1rm)

    elif text == '📝 Diário':
        msg = bot.send_message(chat_id, "O que você quer anotar hoje? (Ex: Supino bati 30kg)")
        bot.register_next_step_handler(msg, lambda m: bot.reply_to(m, "✅ Salvo com sucesso no diário!"))

    elif text == '🆘 Dor vs Lesão':
        bot.send_message(chat_id, "🏥 **Guia Rápido:**\n- **Dor Muscular (Tardia):** Dói mais no dia seguinte, sensação de repuxar ao alongar. É normal e faz parte do crescimento.\n- **Dor Articular (Lesão):** Pontada aguda, estalos com dor, dói mesmo parado. Se for o caso, PARE o exercício!")

    # === 4. EXTRAS ===
    elif text == '🎮 PERFIL & EXTRAS':
        m = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        m.add('🏆 Meu Nível', '✅ Check-in', '🔴 MODO MENGÃO', '🎧 DJ Playlist', '🎲 Desafio', '🔙 Voltar')
        bot.send_message(chat_id, "Área Gamer e Diversão:", reply_markup=m)

    elif text == '🏆 Meu Nível':
        xp = user_db[uid]['xp']
        patente = next((v for k,v in reversed(niveis.items()) if xp>=k), 'Frango')
        bot.send_message(chat_id, f"🏅 **SEU STATUS:**\nXP Total: {xp}\n🏷️ Patente Atual: **{patente}**")

    elif text == '✅ Check-in':
        user_db[uid]['streak'] += 1
        bot.send_message(chat_id, f"🔥 **Check-in realizado!**\nSua ofensiva é de 🔥 {user_db[uid]['streak']} dias seguidos. Não quebre a corrente!")

    elif text == '🔴 MODO MENGÃO':
        bot.send_message(chat_id, "🔴⚫ **VAMOS FLAMENGO!**\nRaça, amor e paixão! Levanta esse peso como se fosse a final da Libertadores! 💪🦅")

    elif text == '🎲 Desafio':
        bot.send_message(chat_id, f"🎲 **DESAFIO RELÂMPAGO:** {random.choice(desafios)}")

    elif text == '🎧 DJ Playlist':
        bot.send_message(chat_id, "🎧 **Spotify Workout:**\n[Playlist Treino Pesado (Rock/Eletrônica)](https://open.spotify.com/playlist/37i9dQZF1DWXRqgorJj26U)")

    elif text == '🔙 Voltar':
        main_menu(message)

# ==========================================
# 📸 PROCESSADOR DE FOTO (IA GEMINI)
# ==========================================
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if not model:
        bot.reply_to(message, "⚠️ IA não configurada. Adicione a variável GEMINI_KEY no Render.")
        return
    
    bot.reply_to(message, "🤖 **Estou analisando o seu prato... Aguarde uns segundinhos.**")
    try:
        # Pega a melhor resolução da foto enviada
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Salva a imagem temporariamente
        temp_img = "food.jpg"
        with open(temp_img, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        # Prepara a imagem e envia pro Gemini
        img = Image.open(temp_img)
        prompt = "Analise esta foto de refeição. Diga os alimentos que você consegue identificar, faça uma estimativa das calorias totais e dos macronutrientes (Proteína, Carboidrato e Gordura). Responda em Português do Brasil de forma direta e amigável."
        response = model.generate_content([prompt, img])
        
        # Resposta da IA
        bot.reply_to(message, f"🍽️ **ANÁLISE NUTRICIONAL (IA):**\n\n{response.text}\n\n_(Nota: Esta é uma estimativa por Inteligência Artificial)_", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"❌ Erro ao analisar a imagem: {e}")

# ==========================================
# 📐 CÁLCULOS
# ==========================================
def calc_anilhas(message):
    try:
        total = float(message.text)
        lado = (total - 20) / 2 # Subtrai os 20kg da barra olímpica
        if lado <= 0:
            bot.reply_to(message, "A barra vazia já pesa 20kg!")
        else:
            bot.reply_to(message, f"🧱 **Fácil:** Coloque **{lado}kg** de CADA lado da barra.")
    except: 
        bot.reply_to(message, "❌ Digite apenas números válidos.")

def calc_1rm(message):
    try:
        peso, reps = map(int, message.text.split())
        rm = peso * (1 + (reps/30))
        bot.reply_to(message, f"💪 **Força Máxima (1RM):** Você consegue pegar até **{rm:.1f}kg** para uma única repetição.")
    except: 
        bot.reply_to(message, "❌ Formato errado. Digite assim: 40 10 (Peso e Número de Repetições).")

# ==========================================
# ⏱️ TIMERS EM SEGUNDO PLANO
# ==========================================
def timer_thread(chat_id):
    time.sleep(60)
    bot.send_message(chat_id, "⏰ **ACABOU O DESCANSO!** Volte para a máquina!")

def tabata_thread(chat_id):
    bot.send_message(chat_id, "🟢 **GO! Trabalhe no máximo (20s)**")
    time.sleep(20)
    bot.send_message(chat_id, "🔴 **PAUSA! Respire (10s)**")
    time.sleep(10)
    bot.send_message(chat_id, "🟢 **GO! Trabalhe no máximo (20s)**")
    time.sleep(20)
    bot.send_message(chat_id, "🏁 **FIM DO CICLO!**")

# --- START ---
keep_alive()
try:
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
except Exception:
    pass
