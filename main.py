import os
import telebot
import time
import random
from telebot import types
from flask import Flask
from threading import Thread

# --- SERVIDOR WEB ---
app = Flask('')

@app.route('/')
def home():
    return "Bot Academia V6 - Gerador Automático!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- CONFIGURAÇÃO ---
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# ==========================================
# 🎲 BANCO DE TREINOS (VARIAÇÕES)
# ==========================================

treinos_variacoes = {
    'A': [
        "🔥 **TREINO A - OPÇÃO 1 (Clássico)**\n\n1. Supino Reto (4x10)\n2. Supino Inclinado (3x12)\n3. Crucifixo (3x15)\n4. Tríceps Corda (4x12)\n5. Tríceps Testa (3x10)",
        "🔥 **TREINO A - OPÇÃO 2 (Halteres)**\n\n1. Supino Reto com Halteres (4x10)\n2. Crucifixo Inclinado (3x12)\n3. Flexão de Braço (3x Falha)\n4. Tríceps Francês (4x12)\n5. Tríceps Banco (3x15)",
        "🔥 **TREINO A - OPÇÃO 3 (Máquinas/Foco)**\n\n1. Supino Máquina (4x12)\n2. Peck Deck (4x15)\n3. Cross Over (3x15)\n4. Tríceps Pulley Barra (4x15)\n5. Tríceps Coice (3x12)"
    ],
    'B': [
        "🦍 **TREINO B - OPÇÃO 1 (Cargas)**\n\n1. Puxada Alta Aberta (4x10)\n2. Remada Curvada (4x8)\n3. Remada Serrote (3x10)\n4. Rosca Direta Barra (4x10)\n5. Rosca Martelo (3x12)",
        "🦍 **TREINO B - OPÇÃO 2 (Detalhes)**\n\n1. Puxada Triângulo (4x12)\n2. Remada Baixa (4x12)\n3. Pulldown (3x15)\n4. Rosca Scott (3x12)\n5. Rosca Concentrada (3x12)",
        "🦍 **TREINO B - OPÇÃO 3 (Rápido)**\n\n1. Barra Fixa (ou Graviton) (3x Falha)\n2. Remada Máquina (3x12)\n3. Voador Inverso (3x15)\n4. Rosca Alternada (3x12)\n5. Antebraço (3x15)"
    ],
    'C': [
        "🍗 **TREINO C - OPÇÃO 1 (Pernas Completas)**\n\n1. Agachamento Livre (4x10)\n2. Leg Press 45 (4x12)\n3. Extensora (3x15)\n4. Stiff (4x12)\n5. Panturrilha em Pé (4x15)",
        "🍗 **TREINO C - OPÇÃO 2 (Foco Posterior)**\n\n1. Mesa Flexora (4x12)\n2. Cadeira Flexora (3x15)\n3. Stiff com Halteres (4x10)\n4. Agachamento Sumô (4x12)\n5. Elevação Pélvica (3x12)",
        "🍗 **TREINO C - OPÇÃO 3 (Ombros e Pernas)**\n\n1. Leg Press Horizontal (4x15)\n2. Passada (3x12)\n3. Desenvolvimento Militar (4x10)\n4. Elevação Lateral (4x15)\n5. Elevação Frontal (3x12)"
    ]
}

# Links GIFs
gifs = {
    'supino': 'https://i.imgur.com/X4Z8tCq.gif', 
    'puxada': 'https://i.imgur.com/0w1PTx8.gif',
    'agachamento': 'https://i.imgur.com/1Tq3Q5S.gif'
}

# --- TIMER ---
def contar_tempo(chat_id):
    time.sleep(60)
    bot.send_message(chat_id, "⏰ ACABOU O DESCANSO! Bora pra próxima série! 💪")

# --- MENUS ---
@bot.message_handler(commands=['start', 'menu'])
def main_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        types.KeyboardButton('🏋️ GERADOR DE TREINO'),
        types.KeyboardButton('⏱️ TIMER 60s'),
        types.KeyboardButton('📝 NOTAS / DIÁRIO'),
        types.KeyboardButton('⚙️ EXTRAS')
    )
    bot.send_message(message.chat.id, "Fala David! Bora gerar um treino novo hoje?", reply_markup=markup)

# --- RESPOSTAS ---
@bot.message_handler(func=lambda message: True)
def bot_message(message):
    text = message.text
    chat_id = message.chat.id

    # === GERADOR DE TREINOS ===
    if text == '🏋️ GERADOR DE TREINO':
        m = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        m.add('Treino A (Peito)', 'Treino B (Costas)', 'Treino C (Pernas)', '🔙 Voltar')
        bot.send_message(chat_id, "Qual grupo muscular vamos treinar hoje?", reply_markup=m)

    elif text == 'Treino A (Peito)':
        enviar_treino(chat_id, 'A')

    elif text == 'Treino B (Costas)':
        enviar_treino(chat_id, 'B')
    
    elif text == 'Treino C (Pernas)':
        enviar_treino(chat_id, 'C')

    # === UTILITÁRIOS ===
    elif text == '⏱️ TIMER 60s':
        bot.send_message(chat_id, "⏳ Contando 60s...")
        Thread(target=contar_tempo, args=(chat_id,)).start()

    elif text == '📝 NOTAS / DIÁRIO':
        bot.send_message(chat_id, "Escreva sua nota (Ex: Carga supino 40kg) que eu salvo aqui (Simulação).")

    elif text == '🔙 Voltar':
        main_menu(message)

# --- FUNÇÃO AUXILIAR PARA ENVIAR O TREINO COM BOTÃO DE TROCAR ---
def enviar_treino(chat_id, tipo):
    # Pega o primeiro treino da lista como padrão
    treino_texto = treinos_variacoes[tipo][0]
    
    markup = types.InlineKeyboardMarkup()
    # Botão de GIF
    if tipo == 'A':
        markup.add(types.InlineKeyboardButton("🎥 Ver GIF Supino", callback_data="supino"))
    elif tipo == 'B':
        markup.add(types.InlineKeyboardButton("🎥 Ver GIF Puxada", callback_data="puxada"))
    elif tipo == 'C':
        markup.add(types.InlineKeyboardButton("🎥 Ver GIF Agachamento", callback_data="agachamento"))
    
    # O BOTÃO MÁGICO DE TROCAR TREINO
    markup.add(types.InlineKeyboardButton(f"🔄 Gerar Outro Treino {tipo}", callback_data=f"trocar_{tipo}"))
    
    bot.send_message(chat_id, treino_texto, parse_mode="Markdown", reply_markup=markup)

# --- CALLBACKS (GIFS E TROCA DE TREINO) ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    # Se for pedido de GIF
    if call.data in gifs:
        bot.answer_callback_query(call.id)
        bot.send_animation(call.message.chat.id, gifs[call.data])
        return

    # Se for pedido de TROCAR TREINO (Logica do Random)
    if call.data.startswith("trocar_"):
        tipo = call.data.split("_")[1] # Pega 'A', 'B' ou 'C'
        novo_treino = random.choice(treinos_variacoes[tipo])
        
        # Monta os botões de novo
        markup = types.InlineKeyboardMarkup()
        if tipo == 'A': markup.add(types.InlineKeyboardButton("🎥 Ver GIF Supino", callback_data="supino"))
        elif tipo == 'B': markup.add(types.InlineKeyboardButton("🎥 Ver GIF Puxada", callback_data="puxada"))
        elif tipo == 'C': markup.add(types.InlineKeyboardButton("🎥 Ver GIF Agachamento", callback_data="agachamento"))
        
        markup.add(types.InlineKeyboardButton(f"🔄 Gerar Outro Treino {tipo}", callback_data=f"trocar_{tipo}"))

        # Edita a mensagem na hora!
        try:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=novo_treino, reply_markup=markup, parse_mode="Markdown")
            bot.answer_callback_query(call.id, "Treino atualizado! 🔄")
        except:
            bot.answer_callback_query(call.id, "Já é esse treino!")

# --- INICIAR ---
keep_alive()
try:
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
except Exception:
    pass
