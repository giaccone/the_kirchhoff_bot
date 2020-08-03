from telegram import ParseMode

def execute(update, context):
    """
    'check_text' reply to selected text messages
    * warn users without username
    * warn users using incorrect terminology

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """

    if update.message.from_user.username is None:
        msg = "Ciao {name}.\n*Per favore imposta uno username* ".format(name=update.message.from_user.name)
        msg += "per facilitare le conversazioni future, grazie.\n\n"
        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
    if 'voltaggio' in update.message.text.lower():
        msg = "Il termine voltaggio, sebbene sia largamente utilizzato *è scorretto*. Ti vieto di utilizzarlo!"
        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
        context.bot.send_photo(chat_id=update.message.chat_id, photo=open('./resources/voltaggio.png', 'rb'))