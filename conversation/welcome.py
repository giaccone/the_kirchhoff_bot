from telegram import InlineKeyboardMarkup
from util.permission import initial_permission
from random import randrange
from util.question_database import question, answer


def execute(update, context):
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
        context.bot.restrictChatMember(chat_id=update.message.chat_id, user_id=member.id,
                                       permissions=initial_permission)

    # send the question
    question_text = "{name}\n".format(name=member.name) + question[context.chat_data[member.id]]
    possible_answers = answer[context.chat_data[member.id]]
    reply_markup = InlineKeyboardMarkup(possible_answers)
    context.bot.send_message(chat_id=update.message.chat_id, text=question_text, reply_markup=reply_markup)