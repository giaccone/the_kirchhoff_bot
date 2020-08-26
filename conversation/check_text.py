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
        if update.message.from_user.id not in context.chat_data:
            context.chat_data[update.message.from_user.id] = 0

        if context.chat_data[update.message.from_user.id] == 0:
            msg = "*primo avviso* (di 3)\n"
            msg += "\n\nCiao {name}.\n*Per favore imposta uno username* ".format(name=update.message.from_user.name)
            msg += "per facilitare le conversazioni future, grazie.\n\n"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            context.chat_data[update.message.from_user.id] = 1
        elif context.chat_data[update.message.from_user.id] == 1:
            msg = "*secondo avviso*\n(di 3)\n"
            msg += "\n\nCiao {name}.\n*Per favore imposta uno username* ".format(name=update.message.from_user.name)
            msg += "per facilitare le conversazioni future, grazie.\n\n"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            context.chat_data[update.message.from_user.id] = 2
        elif context.chat_data[update.message.from_user.id] == 2:
            msg = "*terzo e ultimo avviso*\n"
            msg += "Se non imposti uno username al tuo prossimo messaggio sarai rimosso dal gruppo "
            msg += "(con possibilità di rientrare)\n\n"
            msg += "\n\nCiao {name}.\n*Per favore imposta uno username* ".format(name=update.message.from_user.name)
            msg += "per facilitare le conversazioni future, grazie.\n\n"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            context.chat_data[update.message.from_user.id] = 3
        elif context.chat_data[update.message.from_user.id] == 3:
            msg = "*Sei stato avvisato tre volte*: mi spiace ma fra 15 secondi sarai rimosso dal gruppo."
            msg += "\nRientra quando avrai impostato uno username"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

            # kick the user after a given delay
            def delayed_kick(context):
                context.bot.kickChatMember(chat_id=update.message.chat_id, user_id=update.message.from_user.id)
                context.bot.unbanChatMember(chat_id=update.message.chat_id, user_id=update.message.from_user.id)

            context.job_queue.run_once(delayed_kick, 15)
    else:
        del context.chat_data[update.message.from_user.id]




    if 'voltaggio' in update.message.text.lower():
        msg = "Il termine voltaggio, sebbene sia largamente utilizzato *è scorretto*. Ti vieto di utilizzarlo!"
        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
        context.bot.send_photo(chat_id=update.message.chat_id, photo=open('./resources/voltaggio.png', 'rb'))