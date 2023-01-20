from telegram.constants import ParseMode


async def execute(update, context):
    """
    'help' provides information about the use of the bot

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    msg = "*Ciao*, sono @the\_kirchhoff\_bot .\n\n"
    msg += "Son qui qui prevalentemente per controllare cosa succede.\n"
    msg += "Come utente del gruppo hai a disposizione alcune macro attivabili con il carattere speciale '!'\n\n"
    msg += "prova a scrivere ```!list```"
    

    await context.bot.send_message(chat_id=update.message.chat_id,
                             text=msg,
                             parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)