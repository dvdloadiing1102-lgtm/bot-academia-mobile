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
    return "Bot Academia V9 - YouTube Integrado!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- CONFIGURAÇÃO ---
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# ==========================================
# 📺 LISTA DE TREINOS COM LINKS DO YOUTUBE
# ==========================================
# A sintaxe é: [Nome do Exercício](Link)

treinos_variacoes = {
    'A': [
        (
            "🔥 **TREINO A - OPÇÃO 1 (Clássico)**\n\n"
            "1. [Supino Reto com Barra](https://www.youtube.com/results?search_query=execucao+supino+reto+barra) (4x10)\n"
            "2. [Supino Inclinado Halteres](https://www.youtube.com/results?search_query=execucao+supino+inclinado+halteres) (3x12)\n"
            "3. [Crucifixo Máquina](https://www.youtube.com/results?search_query=execucao+crucifixo+maquina) (3x15)\n"
            "4. [Tríceps Corda](https://www.youtube.com/results?search_query=execucao+triceps+corda) (4x12)\n"
            "5. [Tríceps Testa](https://www.youtube.com/results?search_query=execucao+triceps+testa) (3x10)"
        ),
        (
            "🔥 **TREINO A - OPÇÃO 2 (Halteres)**\n\n"
            "1. [Supino Reto Halteres](https://www.youtube.com/results?search_query=execucao+supino+reto+halteres) (4x10)\n"
            "2. [Crucifixo Inclinado](https://www.youtube.com/results?search_query=execucao+crucifixo+inclinado) (3x12)\n"
            "3. [Flexão de Braço](https://www.youtube.com/results?search_query=execucao+flexao+de+braco) (3x Falha)\n"
            "4. [Tríceps Francês](https://www.youtube.com/results?search_query=execucao+triceps+frances) (4x12)\n"
            "5. [Tríceps Banco](https://www.youtube.com/results?search_query=execucao+triceps+banco) (3x15)"
        )
    ],
    'B': [
        (
            "🦍 **TREINO B - OPÇÃO 1 (Costas/Bíceps)**\n\n"
            "1. [Puxada Alta](https://www.youtube.com/results?search_query=execucao+puxada+alta+polia) (4x10)\n"
            "2. [Remada Curvada](https://www.youtube.com/results?search_query=execucao+remada+curvada) (4x8)\n"
            "3. [Remada Serrote](https://www.youtube.com/results?search_query=execucao+remada+serrote) (3x10)\n"
            "4. [Rosca Direta](https://www.youtube.com/results?search_query=execucao+rosca+direta+barra) (4x10)\n"
            "5. [Rosca Martelo](https://www.youtube.com/results?search_query=execucao+rosca+martelo) (3x12)"
        ),
        (
            "🦍 **TREINO B - OPÇÃO 2 (Volume)**\n\n"
            "1. [Puxada Triângulo](https://www.youtube.com/results?search_query=execucao+puxada+triangulo) (4x12)\n"
            "2. [Remada Baixa](https://www.youtube.com/results?search_query=execucao+remada+baixa+polia) (4x12)\n"
            "3. [Face Pull](https://www.youtube.com/results?search_query=execucao+face+pull) (3x15)\n"
            "4. [Rosca Scott](https://www.youtube.com/results?search_query=execucao+rosca+scott) (3x12)\n"
            "5. [Rosca Concentrada](https://www.youtube.com/results?search_query=execucao+rosca+concentrada) (3x12)"
        )
    ],
    'C': [
        (
            "🍗 **TREINO C - OPÇÃO 1 (Pernas)**\n\n"
            "1. [Agachamento Livre](https://www.youtube.com/results?search_query=execucao+agachamento+livre) (4x10)\n"
            "2. [Leg Press 45](https://www.youtube.com/results?search_query=execucao+leg+press+45) (4x12)\n"
            "3. [Cadeira Extensora](https://www.youtube.com/results?search_query=execucao+cadeira+extensora) (3x15)\n"
            "4. [Stiff](https://www.youtube.com/results?search_query=execucao+stiff) (4x12)\n"
            "5. [Panturrilha em Pé](https://www.youtube.com/results?search_query=execucao+panturrilha+em+pe) (4x15)"
        ),
        (
            "🍗 **TREINO C - OPÇÃO 2 (Foco Posterior)**\n\n"
            "1. [Mesa Flexora](https://www.youtube.com/results?search_query=execucao+mesa+flexora) (4x12)\n"
            "2. [Stiff com Halteres](https://www.youtube.com/results?search_query=execucao+stiff+halteres) (4x10)\n"
            "3. [Agachamento Sumô](https://www.youtube.com/results?search_query=execucao+agachamento+sumo) (4x12)\n"
            "4. [Elevação Pélvica](https://www.youtube.com/results?search_query=execucao+elevacao+pelvica) (3x12)\n"
            "5. [Afundo/Passada](https://www.youtube.com/results?search_query=execucao+afundo+passada) (3x12)"
        )
    ]
}

# Memória Temporária
user_custom_workout = {}

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
        types.KeyboardButton('📝 ESCREVER MEU TREINO'),
        types.KeyboardButton('⚙️ EXTRAS')
    )
    bot.send_message(message.chat.id, "Fala David! Bora treinar?", reply_markup=markup)

# --- RESPOSTAS ---
@bot.message_handler(func=lambda message: True)
def bot_message(message):
    text = message.text
    chat_id = message.chat.id
    user_id = message.from_user.id

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

    elif text == '📝 ESCREVER MEU TREINO':
        msg = bot.send_message(chat_id, "Digita aí: Qual o treino de hoje? (Ex: Correr 20min e 100 flexões)")
        bot.register_next_step_handler(msg, salvar_treino_custom)

    elif text == '⚙️ EXTRAS':
        m = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        m.add('📋 Ver Meu Treino', '🎶 Playlist', '🔙 Voltar')
        bot.send_message(chat_id, "Extras:", reply_markup=m)
    
    elif text == '📋 Ver Meu Treino':
        treino = user_custom_workout.get(user_id, "Nenhum treino salvo hoje!")
        bot.send_message(chat_id, f"📝 **Seu Treino:**\n{treino}", parse_mode="Markdown")

    elif text == '🎶 Playlist':
        bot.send_message(chat_id, "🎧 Playlist Focada: https://open.spotify.com/playlist/37i9dQZF1DX70RN3TfWWJh")

    elif text == '🔙 Voltar':
        main_menu(message)

# --- FUNÇÃO AUXILIAR ---
def salvar_treino_custom(message):
    user_id = message.from_user.id
    user_custom_workout[user_id] = message.text
    bot.reply_to(message, "✅ Salvo! Vá em ⚙️ EXTRAS para ver.")

# --- ENVIAR TREINO (COM TEXTO CLICÁVEL) ---
def enviar_treino(chat_id, tipo):
    treino_texto = treinos_variacoes[tipo][0]
    markup = types.InlineKeyboardMarkup()
    
    # Botão de Trocar (O único botão que sobrou)
    markup.add(types.InlineKeyboardButton(f"🔄 Gerar Outro Treino {tipo}", callback_data=f"trocar_{tipo}"))
    
    # Importante: disable_web_page_preview=True evita que o Telegram mostre 5 janelas de vídeo de uma vez
    bot.send_message(chat_id, treino_texto, parse_mode="Markdown", reply_markup=markup, disable_web_page_preview=True)

# --- CALLBACKS (TROCA DE TREINO) ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data.startswith("trocar_"):
        tipo = call.data.split("_")[1]
        novo_treino = random.choice(treinos_variacoes[tipo])
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(f"🔄 Gerar Outro Treino {tipo}", callback_data=f"trocar_{tipo}"))

        try:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=novo_treino, reply_markup=markup, parse_mode="Markdown", disable_web_page_preview=True)
            bot.answer_callback_query(call.id, "Treino atualizado!")
        except:
            bot.answer_callback_query(call.id, "Já é esse treino!")

# --- INICIAR ---
keep_alive()
try:
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
except Exception:
    pass
