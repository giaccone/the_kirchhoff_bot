from telegram import ParseMode


def execute(update, context):
    """
    'help' provides information about the use of the bot

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    msg = "*Ciao*, sono @the\_kirchhoff\_bot .\n\n"
    msg += "I miei comandi sono:\n"
    msg += " \* /start\n"
    msg += " \* /help\n"
    msg += " \* /r (solo admin)\n"

    context.bot.send_message(chat_id=update.message.chat_id,
                             text=msg,
                             parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)