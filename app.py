from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import logging
from datetime import datetime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Fluxo de criação para bot que responde a comandos:

# Criar uma função que faz algo quando X comando é digitado
async def iniciar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    hora_atual = datetime.now().strftime('%H:%M:%S')
    ano_atual = datetime.now().year
    keyboard = [
        [
            InlineKeyboardButton("Vagas Restantes", callback_data='Restam 10 vagas'),
            InlineKeyboardButton("Horário atual", callback_data=f'O horário atual é {hora_atual}')
        ],
        [
            InlineKeyboardButton("Sair", callback_data='Você escolheu sair')
        ],
        [
            InlineKeyboardButton("Ano atual", callback_data=f'O ano atual é {ano_atual}')
        ]
    ]

    reply_keyboard = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Favor selecionar uma opção:', reply_markup=reply_keyboard)


async def monitorador_de_resposta(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f'Opção escolhida: {query.data}')


async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Para começar a usa o bot digite: "/iniciar ou /start"')


async def horas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    hora_atual = datetime.now().strftime('%H:%M:%S')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Hora atual: {hora_atual}')


async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text.lower() in ('oi', 'olá', 'bom dia', 'tudo bem', 'tudo bem?'):
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Olá seja bem-vindo(a) ao nosso atendimento!', reply_to_message_id=update.message.id)


async def nao_registrado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Esse comando não existe!')

# Criar aplicação e comandos
if __name__ == '__main__':
    # Token da aplicação
    application = ApplicationBuilder().token('6470695012:AAHZulsry6YdT5j6IpRZ9T4PliHX0nGogeM').build()
    # Registrar um handler de comandos(classe que observar se X comando foi digitado)
    # Comando de iniciar e start
    application.add_handler(CommandHandler('iniciar',iniciar))
    application.add_handler(CommandHandler('start',iniciar))
    # Comando de ajuda
    application.add_handler(CommandHandler('ajuda',ajuda))
    # Comando horas
    application.add_handler(CommandHandler('horas',horas))
    # Comando observador de respostas
    application.add_handler(CallbackQueryHandler(monitorador_de_resposta))
    # Comandos não registrados
    application.add_handler(MessageHandler(filters.COMMAND,nao_registrado))
    # Comando de iteração a menssagens
    application.add_handler(MessageHandler(filters.TEXT,responder))
    # "Ligar" o monitoramento de comandos
    application.run_polling()