import os
import telebot
import time
from telebot import types
from flask import Flask
from threading import Thread

# --- CONFIGURAÇÃO PARA O RENDER NÃO DERRUBAR (KEEP ALIVE) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot Academia Online e Roteando!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- INICIALIZAÇÃO DO BOT ---
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# --- FUNÇÃO DO TIMER (EM SEGUNDO PLANO) ---
def contar_tempo(chat_id):
    time.sleep(60) # Espera 60 segundos
    bot.send_message(chat_id, "⏰ ACABOU O DESCANSO!\nBora pra próxima série! 💪")

# --- MENUS ---
@bot.message_handler(commands=['start', 'menu'])
def main_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('🏋️ ÁREA DE TREINO')
    btn2 = types.KeyboardButton('🍎 DIETA E MACROS')
    btn3 = types.KeyboardButton('🤖 PERSONAL IA')
    btn4 = types.KeyboardButton('⚙️ UTILITÁRIOS')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, "Fala Mestre! Escolha a área:", reply_markup=markup)

# --- RESPOSTAS INTELIGENTES ---
@bot.message_handler(func=lambda message: True)
def bot_message(message):
    text = message.text
    chat_id = message.chat.id

    # === 1. ÁREA DE TREINO ===
    if text == '🏋️ ÁREA DE TREINO':
        m = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        m.add('📝 Registrar Carga', '⏱️ Timer 60s', '📅 Treino A', '📅 Treino B', '📅 Treino C', '🔙 Voltar')
        bot.send_message(chat_id, "Opções de Treino:", reply_markup=m)

    elif text == '⏱️ Timer 60s':
        bot.send_message(chat_id, "⏳ Iniciando contagem de 1 minuto... Respira fundo!")
        # Dispara o timer em paralelo para não travar o bot
        Thread(target=contar_tempo, args=(chat_id,)).start()

    elif text == '📅 Treino A':
        treino = (
            "🏋️ **TREINO A (Peito, Ombros e Tríceps):**\n\n"
            "1. Supino Reto (4x 8-12)\n"
            "2. Supino Inclinado Halteres (3x 10-12)\n"
            "3. Crucifixo ou Peck Deck (3x 12-15)\n"
            "4. Desenvolvimento Militar (4x 8-12)\n"
            "5. Elevação Lateral (4x 12-15)\n"
            "6. Tríceps Corda (4x 12-15)\n"
            "7. Tríceps Testa (3x 10-12)"
        )
        bot.send_message(chat_id, treino, parse_mode="Markdown")

    elif text == '📅 Treino B':
        treino = (
            "🦍 **TREINO B (Costas, Bíceps e Trapézio):**\n\n"
            "1. Puxada Alta (4x 10-12)\n"
            "2. Remada Curvada (4x 8-10)\n"
            "3. Remada Serrote (3x 10-12)\n"
            "4. Encolhimento de Ombros (4x 15)\n"
            "5. Rosca Direta (4x 10-12)\n"
            "6. Rosca Martelo (3x 12)\n"
            "7. Rosca Scott (3x 12-15)"
        )
        bot.send_message(chat_id, treino, parse_mode="Markdown")
    
    elif text == '📅 Treino C':
        treino = (
            "🍗 **TREINO C (Pernas Completas):**\n\n"
            "1. Agachamento Livre (4x 8-10)\n"
            "2. Leg Press 45 (4x 10-12)\n"
            "3. Cadeira Extensora (4x 15 - falha)\n"
            "4. Stiff ou Mesa Flexora (4x 12)\n"
            "5. Panturrilha em Pé (5x 15-20)\n"
            "6. Abdominal Infra/Supra (4x 15)"
        )
        bot.send_message(chat_id, treino, parse_mode="Markdown")

    elif text == '📝 Registrar Carga':
        bot.send_message(chat_id, "💪 Para registrar, digite no formato: \n/carga Supino 40kg")

    # === 2. ÁREA DE DIETA ===
    elif text == '🍎 DIETA E MACROS':
        m = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        m.add('🛒 Lista Básica', '💧 Meta Água', '🔙 Voltar')
        bot.send_message(chat_id, "Nutrição:", reply_markup=m)

    elif text == '🛒 Lista Básica':
        lista = (
            "🛒 **Sugestão de Compras Fit:**\n\n"
            "• Ovos e Frango (Proteína base)\n"
            "• Aveia e Arroz (Carbos limpos)\n"
            "• Azeite de Oliva (Gordura boa)\n"
            "• Creatina (Suplemento essencial)\n"
            "• Salada/Vegetais à vontade"
        )
        bot.send_message(chat_id, lista, parse_mode="Markdown")
    
    elif text == '💧 Meta Água':
        bot.send_message(chat_id, "💧 Lembrete: Beba 35ml a 50ml por kg corporal.\nSe você pesa 80kg = ~3 a 4 Litros por dia!")

    # === 3. PERSONAL IA E UTILITÁRIOS ===
    elif text == '🤖 PERSONAL IA':
        m = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        m.add('💡 Dica do Dia', '🔙 Voltar')
        bot.send_message(chat_id, "Dica rápida:", reply_markup=m)
    
    elif text == '💡 Dica do Dia':
        bot.send_message(chat_id, "💡 **Dica:** O sono é anabólico. Dormir menos de 6h prejudica seus ganhos e sua testosterona. Desligue o celular 30min antes de deitar!")

    elif text == '⚙️ UTILITÁRIOS':
        m = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        m.add('💰 Mensalidade', '🔙 Voltar')
        bot.send_message(chat_id, "Financeiro:", reply_markup=m)
    
    elif text == '💰 Mensalidade':
        bot.send_message(chat_id, "💰 Lembrete: Verifique a data de vencimento da sua academia para não ser barrado na catraca!")

    elif text == '🔙 Voltar':
        main_menu(message)

    else:
        # Se digitar algo que não é botão
        if message.text.startswith('/carga'):
            bot.reply_to(message, "✅ Carga registrada temporariamente (Banco de dados em breve)!")
        else:
            bot.send_message(chat_id, "Use os botões do menu para navegar! 🤖")

# --- LOOP PRINCIPAL ANTI-QUEDA ---
keep_alive()
while True:
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"Erro no bot: {e}")
        time.sleep(5)
