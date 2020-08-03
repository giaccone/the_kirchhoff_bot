from util.question_database import question, right_answer
from util.permission import standard_permissions


def execute(update, context):
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
                                         text="Risposta corretta {username}! Buona permanenza nel gruppo!".format(
                                             username=query.from_user.name))
                # restore standard permissions
                context.bot.restrictChatMember(chat_id=query.message.chat_id, user_id=query.from_user.id,
                                               permissions=standard_permissions)
            else:
                msg = "Risposta errata! Entro 15 secondi sarai rimosso dal gruppo.\n"
                msg += "Rientra quando vuoi ma dovrai rispondere correttamente per poter rimanere."
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