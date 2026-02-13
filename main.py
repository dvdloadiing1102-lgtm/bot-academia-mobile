import os
import telebot
from telebot import types
from flask import Flask
from threading import Thread
import time

# --- CONFIGURAÇÃO DO SERVIDOR (PARA O RENDER NÃO DESLIGAR) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot de Academia do David está ONLINE!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- CONFIGURAÇÃO DO BOT ---
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# --- MENUS ---
@bot.message_handler(commands=['start', 'menu'])
def main_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item1 = types.KeyboardButton('🏋️ ÁREA DE TREINO')
    item2 = types.KeyboardButton('🍎 DIETA E MACROS')
    item3 = types.KeyboardButton('🤖 PERSONAL IA')
    item4 = types.KeyboardButton('⚙️ UTILITÁRIOS')
    markup.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id, "Fala Mestre! Escolha a área:", reply_markup=markup)

# --- RESPOSTAS DOS BOTÕES ---
@bot.message_handler(func=lambda message: True)
def bot_message(message):
    text = message.text
    chat_id = message.chat.id

    # 1. ÁREA DE TREINO
    if text == '🏋️ ÁREA DE TREINO':
        m = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        m.add('📝 Registrar Carga', '⏱️ Descanso', '📅 Meu Treino Hoje', '🔙 Voltar')
        bot.send_message(chat_id, "Bora puxar ferro! O que vamos fazer?", reply_markup=m)

    elif text == '📝 Registrar Carga':
        # Aqui simulamos o registro
        bot.send_message(chat_id, "💪 Digite o exercício e a carga (ex: Supino 30kg) que eu vou salvar!")
    
    elif text == '⏱️ Descanso':
        bot.send_message(chat_id, "⏳ Iniciando timer de 60 segundos... Respira!")
        # (Em um bot avançado, usaríamos time.sleep ou job_queue, mas aqui é só resposta rápida)
        
    elif text == '📅 Meu Treino Hoje':
        bot.send_message(chat_id, "📅 Hoje é dia de: PEITO E TRÍCEPS (Exemplo). Foco na execução!")

    # 2. ÁREA DE DIETA
    elif text == '🍎 DIETA E MACROS':
        m = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        m.add('🥩 Registrar Refeição', '💧 Beber Água', '🔙 Voltar')
        bot.send_message(chat_id, "Foco na alimentação! Escolha:", reply_markup=m)

    elif text == '🥩 Registrar Refeição':
        bot.send_message(chat_id, "🍽️ O que você comeu? (Ex: 200g de frango e arroz)")
    
    elif text == '💧 Beber Água':
        bot.send_message(chat_id, "💧 Registrei 500ml de água. Faltam 2L para a meta!")

    # 3. PERSONAL IA
    elif text == '🤖 PERSONAL IA':
        m = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        m.add('💡 Dica do Dia', '🤕 Dor/Lesão', '🔙 Voltar')
        bot.send_message(chat_id, "Sou seu Personal Inteligente. Mande a dúvida:", reply_markup=m)
    
    elif text == '💡 Dica do Dia':
        bot.send_message(chat_id, "💡 Dica: A fase excêntrica (descida) do movimento gera mais hipertrofia. Controle o peso na descida!")

    # 4. UTILITÁRIOS
    elif text == '⚙️ UTILITÁRIOS':
        m = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        m.add('💰 Mensalidade', '🔙 Voltar')
        bot.send_message(chat_id, "Ferramentas extras:", reply_markup=m)
    
    elif text == '💰 Mensalidade':
        bot.send_message(chat_id, "💰 Sua mensalidade vence dia 10. Faltam 5 dias!")

    # COMANDO DE VOLTAR
    elif text == '🔙 Voltar':
        main_menu(message)

    # RESPOSTA PADRÃO
    else:
        bot.send_message(chat_id, "Ainda não entendi esse comando, mas estou aprendendo! Tente usar os botões.")

# --- INICIALIZAÇÃO BLINDADA ---
keep_alive() # Inicia o servidor web falso
try:
    bot.infinity_polling() # Modo infinito para não cair
except Exception as e:
    print(f"Erro no bot: {e}")
