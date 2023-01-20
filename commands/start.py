from telegram.constants import ParseMode


async def execute(update, context):
    """
    'start' provides the start message

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    msg = "Ciao,\nsono @the\_kirchhoff\_bot \n\n"
    msg += "Puoi considerami il professore dei professori di Elettrotecnica ed\n"
    msg += "il mio nome completo è _Gustav Robert Kirchhoff_."

    await context.bot.send_message(chat_id=update.message.chat_id,
                             text=msg,
                             parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)