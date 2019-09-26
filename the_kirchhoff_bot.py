# modules
# =======
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import telegram as telegram

# other modules
# ------------ 
from functools import wraps
import logging
from random import randrange

# preamble code
# =============

# set basic logging
# -----------------
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# global question database
# ------------------------
question = {0:"Qual'è l'unità di misura della tensione?"}
answer = {0:[[telegram.InlineKeyboardButton("metri (m)", callback_data="metri (m)"),
                telegram.InlineKeyboardButton("joule (J)", callback_data="joule (J)")],
                [telegram.InlineKeyboardButton("volt (V)", callback_data="volt (V)"),
                telegram.InlineKeyboardButton("newton (N)", callback_data="newton (N)")]]}
right_answer = {0:"volt (V)"}


# admin list
# ----------
fid = open('./admin_only/admin_list.txt', 'r')
LIST_OF_ADMINS = [int(adm) for adm in fid.readline().split()]
fid.close()


# utility functions
# -----------------
def read_token(filename):
    """
    'read_token' reads the bot token from a text file.

    :param filename: filename of the file including the token
    :return: string with the token
    """
    with open(filename) as f:
        token = f.readline().replace('\n', '')
    return token


def restricted(func):
    """
    'restricted' decorates a function so that it can be used only to allowed users

    :param func: function to be decorated
    :return: function wrapper
    """
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            print("Unauthorized access denied for {}.".format(user_id))
            context.bot.send_message(chat_id=update.message.chat_id, text="You are not authorized to run this command")
            return
        return func(update, context, *args, **kwargs)
    return wrapped


def start(update, context):
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
                     parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
    fid.close()


def help(update, context):
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
                     parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)


def welcome_message(update, context):
    """
    'welcome_message' generated the message sent to new users joining the group

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """

    # welcome message
    for member in update.message.new_chat_members:
        msg = ""
        if member.username is None:
            msg += "Benvenuto {name}. Per prima cosa imposta uno username ".format(name=member.name)
            msg += "per facilitare le conversazioni future, grazie.\n\n"
            msg += "Inoltre, per poter rimanere dovrai rispondere correttamente alla seguente domanda.\n"
            msg += "(Se sbagli sarai rimosso dal gruppo con possibilità di rientrare quando vuoi)."
        else:
            msg += "Ciao {username}!\n".format(username=member.username)
            msg += "Benvenuto nel gruppo. Per poter rimanere dovrai rispondere alla seguente domanda.\n"
            msg += "(Se sbagli sarai rimosso dal gruppo con possibilità di rientrare quando vuoi)."
        update.message.reply_text(msg)

        # update chat_data with the used_id and the index of its question
        context.chat_data[member.id] = randrange(len(question))

    # send the question
    question_text = "{name}\n".format(name=member.name) + question[context.chat_data[member.id]]
    possible_answers = answer[context.chat_data[member.id]]
    reply_markup = telegram.InlineKeyboardMarkup(possible_answers)
    context.bot.send_message(chat_id=update.message.chat_id, text=question_text, reply_markup=reply_markup)


def answer_check(update, context):
    """
    'answer_check' reacts to an InlineKeyboardButton pressure.
    It evaluates if the answer is True or False.

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    # get query
    query = update.callback_query
    
    
    # check if the user is in chat_data (i.e. he is expected to answer)
    if query.from_user.id in context.chat_data:
        # check if user is answering to his own question
        if query.message.reply_markup.inline_keyboard == answer[context.chat_data[query.from_user.id]]:
            
            # send selected answer
            context.bot.edit_message_text(text="Hai hai scelto: {}".format(query.data),
                                        chat_id=query.message.chat_id,
                                        message_id=query.message.message_id)
            
            # check correctness
            if query.data == right_answer[context.chat_data[query.from_user.id]]:
                context.bot.send_message(chat_id=query.message.chat_id, text="Risposta corretta! Buona permanenza nel gruppo!")
            else:
                msg = "Risposta errata! Entro 15 secondi sarai rimosso dal gruppo.\n"
                msg +="Rientra quando vuoi ma dovrai rispondere correttamente per poter rimanere."
                context.bot.send_message(chat_id=query.message.chat_id, text=msg)
                # kick the user after a given delay
                def delayed_kick(context, query=query):
                    context.bot.kickChatMember(chat_id=query.message.chat_id, user_id=query.from_user.id)
                    context.bot.unbanChatMember(chat_id=query.message.chat_id, user_id=query.from_user.id)
                context.job_queue.run_once(delayed_kick, 15)
                
            del context.chat_data[query.from_user.id]

        else:
            msg = "@{username} questa non è la tua domanda.".format(username=query.from_user.name)
            context.bot.send_message(chat_id=query.message.chat_id, text=msg)
    
    else:
        msg = "@{username} tu hai già risposto.".format(username=query.from_user.name)
        context.bot.send_message(chat_id=query.message.chat_id, text=msg)


@restricted
def send(update, context):
    """
    'send' send a message in the group through the bot
    usage: /send message of the text

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    print(update.message)
    print("\n\n")
    print(update.message.reply_to_message)
    print("\n\n")
    print(hasattr(update.message, 'reply_to_message'))
    msg = update.message.text.replace('/send ','').replace('\*','*'). replace('\_','_')
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
    if update.message.reply_to_message is None:
        context.bot.send_message(chat_id=update.message.chat_id,
                                text=msg,
                                parse_mode=telegram.ParseMode.MARKDOWN,
                                disable_web_page_preview=True)
    else:
        context.bot.send_message(chat_id=update.message.chat_id,
                                text=msg,
                                parse_mode=telegram.ParseMode.MARKDOWN,
                                disable_web_page_preview=True,
                                reply_to_message_id=update.message.reply_to_message.message_id)


@restricted
def kick(update, context):
    """
    'kick' kick user out from the group
    usage: /send message of the text

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    user_id = update.message.reply_to_message.from_user.id
    context.bot.kickChatMember(chat_id=update.message.chat_id, user_id=user_id)
    context.bot.unbanChatMember(chat_id=update.message.chat_id, user_id=user_id)


@restricted
def ban(update, context):
    """
    'kick' kick user out from the group
    usage: /send message of the text

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    user_id = update.message.reply_to_message.from_user.id
    context.bot.kickChatMember(chat_id=update.message.chat_id, user_id=user_id)


# bot - main
# ==========
def main():
    # set TOKEN and initialization
    fname = './admin_only/the_kirchhoff_bot_token.txt'
    updater = Updater(token=read_token(fname), use_context=True)
    dispatcher = updater.dispatcher

    # restart - restart the BOT
    # -------------------------
    def stop_and_restart():
        """Gracefully stop the Updater and replace the current process with a new one"""
        updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    @restricted
    def restart(update, context):
        update.message.reply_text('Bot is restarting...')
        Thread(target=stop_and_restart).start()
    
    # /r - restart the bot
    dispatcher.add_handler(CommandHandler('r', restart))

    # /start handler
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # /help handler
    help_handler = CommandHandler('help', help)
    dispatcher.add_handler(help_handler)

    # welcome message
    add_group_handle = MessageHandler(Filters.status_update.new_chat_members, welcome_message)
    dispatcher.add_handler(add_group_handle)
    updater.dispatcher.add_handler(CallbackQueryHandler(answer_check))

    # /send handler
    send_handler = CommandHandler('send', send)
    dispatcher.add_handler(send_handler)

    # /kick handler
    kick_handler = CommandHandler('kick', kick)
    dispatcher.add_handler(kick_handler)

    # /ban handler
    ban_handler = CommandHandler('kick', ban)
    dispatcher.add_handler(kick_handler)

    # start the BOT
    updater.start_polling()
    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


# run the bot
# ===========
if __name__ == '__main__':
    main()