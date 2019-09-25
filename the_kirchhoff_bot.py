 
# modules
# =======
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import telegram as telegram
# other modules
# ------------ 
from functools import wraps

# preamble code
# =============

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