from telegram import ParseMode


def execute(update, context):
    """
    'start' provides the start message

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    msg = "*Ciao*, sono @the\_kirchhoff\_bot \n\n"
    msg += "Sono qui per aiutarti a gestire il tuo gruppo Telegram."

    context.bot.send_message(chat_id=update.message.chat_id,
                             text=msg,
                             parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)