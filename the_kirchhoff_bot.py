# modules
# =======
import os
import sys
from threading import Thread
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from config import TOKEN
import commands as cmd
import conversation as cnv
from util.decorators import restricted

# other modules
# ------------
import logging

# set basic logging
# -----------------
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


# bot - main
# ==========
def main():
    # set TOKEN and initialization
    updater = Updater(token=TOKEN, use_context=True)
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
    start_handler = CommandHandler('start', cmd.start.execute)
    dispatcher.add_handler(start_handler)

    # /help handler
    help_handler = CommandHandler('help', cmd.help.execute)
    dispatcher.add_handler(help_handler)

    # /send handler
    send_handler = CommandHandler('send', cmd.send.execute)
    dispatcher.add_handler(send_handler)

    # /kick handler
    kick_handler = CommandHandler('kick', cmd.kick.execute)
    dispatcher.add_handler(kick_handler)

    # /ban handler
    ban_handler = CommandHandler('ban', cmd.ban.execute)
    dispatcher.add_handler(ban_handler)

    # /rm handler
    rm_handler = CommandHandler('rm', cmd.rm.execute)
    dispatcher.add_handler(rm_handler)

    # /rm_inactive handler
    rm_inactive_handler = CommandHandler('rm_inactive', cmd.cg.execute)
    dispatcher.add_handler(rm_inactive_handler)

    # /poll handler
    poll_handler = CommandHandler('poll', cmd.poll.execute)
    dispatcher.add_handler(poll_handler)

    # /spoll handler
    spoll_handler = CommandHandler('spoll', cmd.spoll.execute)
    dispatcher.add_handler(spoll_handler)

    # /cpoll handler
    end_handler = CommandHandler('end', cmd.end.execute)
    dispatcher.add_handler(end_handler)

    # /job_list handler
    job_list_handler = CommandHandler('job_list', cmd.job_list.execute)
    dispatcher.add_handler(job_list_handler)

    # /job_stop handler
    job_stop_handler = CommandHandler('job_stop', cmd.job_stop)
    dispatcher.add_handler(job_stop_handler)

    # /pin handler
    pin_handler = CommandHandler('pin', cmd.pin.execute)
    dispatcher.add_handler(pin_handler)

    # /pin handler
    send_file_handler = CommandHandler('send_file', cmd.send_file.execute)
    dispatcher.add_handler(send_file_handler)
    
    # welcome
    add_group_handle = MessageHandler(Filters.status_update.new_chat_members, cnv.welcome.execute)
    dispatcher.add_handler(add_group_handle)
    updater.dispatcher.add_handler(CallbackQueryHandler(cnv.answer_check.execute))

    # check_text
    check_text_handle = MessageHandler(Filters.text, cnv.check_text.execute)
    dispatcher.add_handler(check_text_handle)

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
