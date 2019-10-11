# modules
# =======
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import telegram as telegram
import datetime

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
            9:"Qual'è l'unità di misura della frequenza?"}
answer = {0:generate_buttons(['metri (m)', 'joule (J)', 'volt (V)', 'newton (N)']),
          1:generate_buttons(['16', '5', '9', '25']),
          2:generate_buttons(['ampere (A)', 'watt (W)', 'Farad (F)', 'weber (Wb)']),
          3:generate_buttons(['watt (W)', 'joule (J)', 'pascal (Pa)', 'kelvin (K)']),
          4:generate_buttons(['log(x)', '1/tan(x)', '-cos(x)', 'cos(x)']),
          5:generate_buttons(['k2+k1', 'k1', 'k2', 'k1*k2']),
          6:generate_buttons(['0', '1', 'infinito', '-1']),
          7:generate_buttons(['V', 'kg', 'm/V', 'V/m']),
          8:generate_buttons(['rad', 'A/m', 'm2', 'Hz']),
          9:generate_buttons(['m', 'Wb', 'Hz', '°C'])}
right_answer = {0:"volt (V)",
                1:"5",
                2:"ampere (A)",
                3:"watt (W)",
                4:"cos(x)",
                5:"k1",
                6:"0",
                7:"V/m",
                8:"A/m",
                9:"Hz"}


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


@restricted
def send(update, context):
    """
    'send' send a message in the group through the bot
    usage: /send message of the text

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
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
    'ban' ban user out from the group

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    user_id = update.message.reply_to_message.from_user.id
    context.bot.kickChatMember(chat_id=update.message.chat_id, user_id=user_id)


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

@restricted
def rm(update, context):
    """
    'rm' remove messages
    usage: /rm or /rm number_of_messages

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """

    text = update.message.text.split()
    if len(text) > 1:
        n_msg = int(text[1]) + 1
        first_id = update.message.message_id
        k = 0
        c = 0

        while k <= n_msg:
            del_id = first_id - k - c
            
            try:
                context.bot.delete_message(chat_id=update.message.chat_id, message_id=del_id)
                k += 1
            except telegram.error.TelegramError:
                c += 1

    else:
        context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.reply_to_message.message_id)   
        # remove command
        context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)


def esame(update, context):
    """
    'esame' gives information about the exam

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """

    # all messages generated here will be deleted after the delay_time
    delay_time = 30 # sec

    # set message
    msg = "Buongiorno {}\n".format(update.message.from_user.name)
    msg = msg.replace("_","\_")
    msg += "L'esme è composto da:\n \* prova scritta (obbligatoria)\n \* prova orale obbligatoria\n\n"
    msg += "tutti i dettagli a questo [link](https://didattica.polito.it/pls/portal30/gap.pkg_guide.viewGap?p_cod_ins=01JWDMN&p_a_acc=2020&p_header=S&p_lang=IT)"
    msg += "\n\nQuesto messaggio si \nautodistruggerà tra {} secondi (salvati il link)".format(delay_time)

    # send message
    sent_msg = context.bot.send_message(chat_id=update.message.chat_id,
                     text=msg,
                     parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
    
    # clean chat deleting the message after 30 sec
    def delayed_delete(context, message_id=[sent_msg.message_id, update.message.message_id]):
        
        for msg_id in message_id:
            context.bot.delete_message(chat_id=update.message.chat_id, message_id=msg_id)
    context.job_queue.run_once(delayed_delete, delay_time)


def orario(update, context):
    """
    'orario' send timetable

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    # all messages generated here will be deleted after the delay_time
    delay_time = 30 # sec

    # set message
    msg = "Buongiorno {}\n".format(update.message.from_user.name)
    msg = msg.replace("_","\_")
    msg +="A questo link trovi il calendario: [link](https://calendar.google.com/calendar/embed?src=22m0uulcsk95n1nf22o3s7mt3g%40group.calendar.google.com&ctz=Europe%2FRome)\n"
    msg +="\nQuesto messaggio si autodistruggerà tra {} secondi (salvati il link)".format(delay_time)

    # send message
    sent_msg = context.bot.send_message(chat_id=update.message.chat_id,
                     text=msg,
                     parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)

    # clean chat deleting the message after 30 sec
    def delayed_delete(context, message_id=[sent_msg.message_id, update.message.message_id]):
        
        for msg_id in message_id:
            context.bot.delete_message(chat_id=update.message.chat_id, message_id=msg_id)
    context.job_queue.run_once(delayed_delete, delay_time)
    

@restricted
def rm_inactive(update, context):
    """
    'rm_inactive' remove inactive users

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    for member in context.chat_data:
        context.bot.kickChatMember(chat_id=update.message.chat_id, user_id=member)
        context.bot.unbanChatMember(chat_id=update.message.chat_id, user_id=member)

@restricted
def poll(update, context):
    """
    'poll' create a new poll

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    msg = update.message.text.replace('/poll ','').split(";")
    question = msg[0]
    options = msg[1:]
    context.bot.send_poll(chat_id=update.message.chat_id,
                     question=question,
                     options=options,
                     disable_notification=False)

    
    # remove command
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)


@restricted
def spoll(update, context):
    """
    'spoll' schedule a new poll

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    poll_data, date_name = update.message.text.split('_end_')
    date, name = date_name.split('_name_')
    msg = poll_data.replace('/spoll ','').split(";")
    date = [int(k) for k in date.split(";")]
    
    question = msg[0]
    options = msg[1:]
    def poll_now(context, update=update):
        msg_poll = context.bot.send_poll(chat_id=update.message.chat_id,
                        question=question,
                        options=options,
                        disable_notification=False)
        
        context.bot.pin_chat_message(chat_id=update.message.chat_id, message_id=msg_poll.message_id, disable_notification=False)
        
    
    time = datetime.datetime(date[0], date[1], date[2], date[3], date[4], 0, 0)
    context.job_queue.run_once(poll_now, time, name=name)

    
    # remove command
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)


@restricted
def end(update, context):
    """
    'end' close an existing poll

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    context.bot.stop_poll(chat_id=update.message.chat_id, message_id=update.message.reply_to_message.message_id)

    # remove command
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)


@restricted
def job_list(update, context):
    """
    'job_list' send a job list to the admin

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    msg = ""
    for k, j in enumerate(context.job_queue.jobs()):
        msg += "job {}: {} , removed={}\n".format(k, j.name, j.removed)

    for adm in LIST_OF_ADMINS:
        chat_id = int(adm)
        try:
            context.bot.send_message(chat_id=chat_id, text=msg)
        except telegram.error.TelegramError:
            pass
    
    # remove command
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)


@restricted
def job_stop(update, context):
    """
    'job_stop' stops a job

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    jobs = update.message.text.replace("/job_stop","")
    jobs = jobs.split(";")
    for jname in jobs:
        j = context.job_queue.get_jobs_by_name(jname.strip())
        for ele in j:
            ele.schedule_removal()


@restricted
def pin(update, context):
    """
    'pin' a message

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """

    # pin message
    context.bot.pin_chat_message(chat_id=update.message.chat_id, message_id=update.message.reply_to_message.message_id, disable_notification=False)  

    # remove command
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)


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

    # check_text
    check_text_handle = MessageHandler(Filters.text, check_text)
    dispatcher.add_handler(check_text_handle)

    # /send handler
    send_handler = CommandHandler('send', send)
    dispatcher.add_handler(send_handler)

    # /kick handler
    kick_handler = CommandHandler('kick', kick)
    dispatcher.add_handler(kick_handler)

    # /ban handler
    ban_handler = CommandHandler('ban', ban)
    dispatcher.add_handler(ban_handler)

    # /rm handler
    rm_handler = CommandHandler('rm', rm)
    dispatcher.add_handler(rm_handler)

    # /esame handler
    esame_handler = CommandHandler('esame', esame)
    dispatcher.add_handler(esame_handler)

    # /orario handler
    orario_handler = CommandHandler('orario', orario)
    dispatcher.add_handler(orario_handler)

    # /rm_inactive handler
    rm_inactive_handler = CommandHandler('rm_inactive', rm_inactive)
    dispatcher.add_handler(rm_inactive_handler)

    # /poll handler
    poll_handler = CommandHandler('poll', poll)
    dispatcher.add_handler(poll_handler)

    # /spoll handler
    spoll_handler = CommandHandler('spoll', spoll)
    dispatcher.add_handler(spoll_handler)

    # /cpoll handler
    end_handler = CommandHandler('end', end)
    dispatcher.add_handler(end_handler)

    # /job_list handler
    job_list_handler = CommandHandler('job_list', job_list)
    dispatcher.add_handler(job_list_handler)

    # /job_stop handler
    job_stop_handler = CommandHandler('job_stop', job_stop)
    dispatcher.add_handler(job_stop_handler)

    # /pin handler
    pin_handler = CommandHandler('pin', pin)
    dispatcher.add_handler(pin_handler)

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