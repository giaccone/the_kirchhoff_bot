# import token
from config import TOKEN
# import commands
import commands as cmd
import conversation as cnv
# PTB modules
from telegram.ext import ApplicationBuilder, CommandHandler
from telegram.ext import MessageHandler, filters, CallbackQueryHandler

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
    # initialize bot
    application = ApplicationBuilder().token(TOKEN).build()

    # /start handler
    start_handler = CommandHandler('start', cmd.start.execute)
    application.add_handler(start_handler)

    # /help handler
    help_handler = CommandHandler('help', cmd.help.execute)
    application.add_handler(help_handler)

    # /help handler
    test_handler = CommandHandler('test', cmd.test.execute)
    application.add_handler(test_handler)

    # /send handler
    send_handler = CommandHandler('send', cmd.send.execute)
    application.add_handler(send_handler)

    # /kick handler
    kick_handler = CommandHandler('kick', cmd.kick.execute)
    application.add_handler(kick_handler)

    # /ban handler
    ban_handler = CommandHandler('ban', cmd.ban.execute)
    application.add_handler(ban_handler)

    # /rm handler
    rm_handler = CommandHandler('rm', cmd.rm.execute)
    application.add_handler(rm_handler)

    # /rm_inactive handler
    rm_inactive_handler = CommandHandler('rm_inactive', cmd.cg.execute)
    application.add_handler(rm_inactive_handler)

    # /poll handler
    poll_handler = CommandHandler('poll', cmd.poll.execute)
    application.add_handler(poll_handler)

    # /spoll handler
    spoll_handler = CommandHandler('spoll', cmd.spoll.execute)
    application.add_handler(spoll_handler)

    # /end handler
    end_handler = CommandHandler('end', cmd.end.execute)
    application.add_handler(end_handler)

    # /job_list handler
    job_list_handler = CommandHandler('job_list', cmd.job_list.execute)
    application.add_handler(job_list_handler)

    # /job_stop handler
    job_stop_handler = CommandHandler('job_stop', cmd.job_stop.execute)
    application.add_handler(job_stop_handler)

    # /pin handler
    pin_handler = CommandHandler('pin', cmd.pin.execute)
    application.add_handler(pin_handler)

    # /send_file handler
    send_file_handler = CommandHandler('send_file', cmd.send_file.execute)
    application.add_handler(send_file_handler)

    # /send_image handler
    send_image_handler = CommandHandler('send_image', cmd.send_image.execute)
    application.add_handler(send_image_handler)
    
    # welcome
    add_group_handle = MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, cnv.welcome.execute)
    application.add_handler(add_group_handle)

    # query reaction for inline buttons
    # updater.dispatcher.add_handler(CallbackQueryHandler(cnv.query_reaction.execute))
    application.add_handler(CallbackQueryHandler(cnv.query_reaction.execute))

    # check_text
    check_text_handle = MessageHandler(filters.TEXT, cnv.check_text.execute)
    application.add_handler(check_text_handle)

    # start the BOT
    application.run_polling()


# run the bot
# ===========
if __name__ == '__main__':
    main()
