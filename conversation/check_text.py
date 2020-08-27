from telegram import ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from util.permission import initial_permission
import time

def execute(update, context):
    """
    'check_text' reply to selected text messages
    * warn users without username
    * warn users using incorrect terminology

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """

    # check if user have a username
    if update.message.from_user.username is None:
        # check if the user have already been warned about missing username
        if update.message.from_user.id not in context.chat_data:
            # chat_data is used to register the number of warnings
            context.chat_data[update.message.from_user.id] = 0

        # first warning
        if context.chat_data[update.message.from_user.id] == 0:
            msg = "*primo avviso* (di 3)\n"
            msg += "\n\nCiao {name}.\n*Per favore imposta uno username* ".format(name=update.message.from_user.name)
            msg += "per facilitare le conversazioni future, grazie.\n\n"
            msg += "Cerca su Google come fare o clicca qui --> [link](https://bfy.tw/OtDz)".format(
                name=update.message.from_user.name)
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
            # update number of warnings
            context.chat_data[update.message.from_user.id] = 1
        # second warning
        elif context.chat_data[update.message.from_user.id] == 1:
            msg = "*secondo avviso* (di 3)\n"
            msg += "\n\nCiao {name}.\n*Per favore imposta uno username* ".format(name=update.message.from_user.name)
            msg += "per facilitare le conversazioni future, grazie.\n\n"
            msg += "Cerca su Google come fare o clicca qui --> [link](https://bfy.tw/OtDz)".format(
                name=update.message.from_user.name)
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
            # update number of warnings
            context.chat_data[update.message.from_user.id] = 2
        # third warning
        elif context.chat_data[update.message.from_user.id] == 2:
            msg = "*terzo e ultimo avviso*\n"
            msg += "Se non imposti uno username al tuo prossimo messaggio ti saranno revocati i permessi di scrivere nel gruppo.\n\n"
            msg += "Cerca su Google come fare o clicca qui --> [link](https://bfy.tw/OtDz)".format(name=update.message.from_user.name)
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
            # update number of warnings
            context.chat_data[update.message.from_user.id] = 3
        # after third warning (above) the user permission are restricted
        elif context.chat_data[update.message.from_user.id] == 3:
            msg = "*Sei stato avvisato tre volte*: mi spiace ma fra 15 secondi sarai rimosso dal gruppo."
            msg += "\nRientra quando avrai impostato uno username"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

            # prepare a button fro the user to notify that he has set the username
            buttons = [[InlineKeyboardButton("Ok, ho impostato uno username.", callback_data="I'm ready")]]
            reply_markup = InlineKeyboardMarkup(buttons)
            msg = "D'ora in poi non puoi più scrivere messaggi. Verrai nuovamente abilitato"
            msg += " solo dopo aver impostato uno username\n\n"
            msg += "Cerca su Google come fare o clicca qui --> [link](https://bfy.tw/OtDz)".format(name=update.message.from_user.name)
            msg += "\n\nQuando lo hai fatto premi il pulsante seguente:"
            time.sleep(0.5)
            context.bot.send_message(chat_id=update.message.chat_id, text=msg,
                                     reply_markup=reply_markup, disable_web_page_preview=True)

            # bind the user to its button using chat_data
            context.chat_data[update.message.message_id + 2] = update.message.from_user.id
            context.bot.restrictChatMember(chat_id=update.message.chat_id, user_id=update.message.from_user.id,
                                           permissions=initial_permission)

    if 'voltaggio' in update.message.text.lower():
        msg = "Il termine voltaggio, sebbene sia largamente utilizzato *è scorretto*. Ti vieto di utilizzarlo!"
        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
        context.bot.send_photo(chat_id=update.message.chat_id, photo=open('./resources/voltaggio.png', 'rb'))