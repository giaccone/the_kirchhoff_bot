# modules
# =======
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import telegram as telegram
from config import LIST_OF_ADMINS, TOKEN
import commands as cmd
from util.decorators import restricted

# other modules
# ------------
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
def generate_buttons(labels):
    buttons = [[telegram.InlineKeyboardButton(labels[0], callback_data=labels[0]),
                telegram.InlineKeyboardButton(labels[1], callback_data=labels[1])],
                [telegram.InlineKeyboardButton(labels[2], callback_data=labels[2]),
                telegram.InlineKeyboardButton(labels[3], callback_data=labels[3])]]
    return buttons

question = {0:"Qual'è l'unità di misura della tensione elettrica?",
            1:"Qual'è il modulo del numero complesso 4+i3 ?",
            2:"Qual'è l'unità di misura della corrente elettrica?",
            3:"Qual'è l'unità di misura della potenza?",
            4:"Qual'è la derivata di sin(x) rispetto a x?",
            5:"Sia f(x)=k1*x + k2. Qual'è la derivata di f(x) rispetto a x?",
            6:"Quanto vale il valor medio di sin(x) calcolato su un periodo?",
            7:"Qual'è l'unità di misura del campo elettrico?",
            8:"Qual'è l'unità di misura del campo magnetico?",
            9:"Qual'è l'unità di misura della frequenza?",
            10:"Come si calcola l'energia cinetica?",
            11:"Se f è una funzione lineare ed f(x1) vale 5. Quanto vale f(5 x1)?",
            12:"Sia f una funzione periodica. Il suo integrale su un periodo vale 10. Quanto vale l'integrale su tre periodi?",
            13:"20°C, espressi in kelvin, sono pari a:",
            14:"Durante la fase di evaporazione, la temperatura dell'acqua:"}
answer = {0:generate_buttons(['metri (m)', 'joule (J)', 'volt (V)', 'newton (N)']),
          1:generate_buttons(['16', '5', '9', '25']),
          2:generate_buttons(['ampere (A)', 'watt (W)', 'Farad (F)', 'weber (Wb)']),
          3:generate_buttons(['watt (W)', 'joule (J)', 'pascal (Pa)', 'kelvin (K)']),
          4:generate_buttons(['log(x)', '1/tan(x)', '-cos(x)', 'cos(x)']),
          5:generate_buttons(['k2+k1', 'k1', 'k2', 'k1*k2']),
          6:generate_buttons(['0', '1', 'infinito', '-1']),
          7:generate_buttons(['V', 'kg', 'm/V', 'V/m']),
          8:generate_buttons(['rad', 'A/m', 'm2', 'Hz']),
          9:generate_buttons(['m', 'Wb', 'Hz', '°C']),
          10:generate_buttons(['mv', '0.5 m v^2', 'm g h', 'v^2/2']),
          11:generate_buttons(['1', '5', '25', '0.5']),
          12:generate_buttons(['10', '3.3', '15', '30']),
          13:generate_buttons(['-273.15 K', '293.15 K','10000 K','-20 K']),
          14:generate_buttons(['aumenta', 'è costante', 'diminuisce', 'vale 100 K'])}
right_answer = {0:"volt (V)",
                1:"5",
                2:"ampere (A)",
                3:"watt (W)",
                4:"cos(x)",
                5:"k1",
                6:"0",
                7:"V/m",
                8:"A/m",
                9:"Hz",
                10:"0.5 m v^2",
                11:"25",
                12:"30",
                13:"293.15 K",
                14:"è costante"}


# common permissions
# ------------------
initial_permission = telegram.ChatPermissions(can_send_messages=False)
standard_permissions = telegram.ChatPermissions(can_send_messages=True,
                can_send_media_messages=True,
                can_send_polls=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_change_info=False,
                can_invite_users=False,
                can_pin_messages=False)


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
        # remove permissions
        context.bot.restrictChatMember(chat_id=update.message.chat_id, user_id=member.id, permissions=initial_permission)
        

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
        idx = query.message.text.index("\n") + 1
        if query.message.text[idx:] == question[context.chat_data[query.from_user.id]]:
            
            # send selected answer
            context.bot.edit_message_text(text="Hai hai scelto: {}".format(query.data),
                                        chat_id=query.message.chat_id,
                                        message_id=query.message.message_id)
            
            # check correctness
            if query.data == right_answer[context.chat_data[query.from_user.id]]:
                context.bot.send_message(chat_id=query.message.chat_id,
                    text="Risposta corretta {username}! Buona permanenza nel gruppo!".format(username=query.from_user.name))
                # restore standard permissions
                context.bot.restrictChatMember(chat_id=query.message.chat_id, user_id=query.from_user.id, permissions=standard_permissions)
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
            msg = "{username} questa non è la tua domanda.".format(username=query.from_user.name)
            context.bot.send_message(chat_id=query.message.chat_id, text=msg)
    
    else:
        msg = "{username} tu hai già risposto.".format(username=query.from_user.name)
        context.bot.send_message(chat_id=query.message.chat_id, text=msg)


def check_text(update, context):
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
        update.message.reply_text(msg, parse_mode=telegram.ParseMode.MARKDOWN)
    if 'voltaggio' in update.message.text.lower():
        msg = "Il termine voltaggio, sebbene sia largamente utilizzato *è scorretto*. Ti vieto di utilizzarlo!"
        update.message.reply_text(msg, parse_mode=telegram.ParseMode.MARKDOWN)
        context.bot.send_photo(chat_id=update.message.chat_id, photo=open('./resources/voltaggio.png', 'rb'))


# bot - main
# ==========
def main():
    # set TOKEN and initialization
    fname = './admin_only/the_kirchhoff_bot_token.txt'
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
    
    # welcome message
    add_group_handle = MessageHandler(Filters.status_update.new_chat_members, welcome_message)
    dispatcher.add_handler(add_group_handle)
    updater.dispatcher.add_handler(CallbackQueryHandler(answer_check))

    # check_text
    check_text_handle = MessageHandler(Filters.text, check_text)
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
