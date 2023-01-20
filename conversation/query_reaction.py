from util.question_database import right_answer
from util.permission import standard_permissions
import asyncio


async def execute(update, context):
    """
    'answer_check' reacts to an InlineKeyboardButton pressure.
    It evaluates if the answer is True or False.

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """

    # get query
    query = update.callback_query

    if "Quando lo hai fatto premi il pulsante seguente:" in query.message.text:
        if context.chat_data[query.message.message_id] == query.from_user.id:
            if query.from_user.username is None:
                await context.bot.send_message(chat_id=query.message.chat_id,
                                        text="Ti avevo detto di inserire uno username {}".format(query.from_user.name))
            else:
                await context.bot.send_message(chat_id=query.message.chat_id,
                                        text="Grazie per aver impostato il tuo username {}.\n\nSei nuovamente abilitato a scrivere.".format(query.from_user.name))
                # restore standard permissions
                await context.bot.restrict_chat_member(chat_id=query.message.chat_id, user_id=query.from_user.id,
                                            permissions=standard_permissions)
                del context.chat_data[query.from_user.id]
        else:
            await context.bot.send_message(chat_id=query.message.chat_id,
                                    text="Non sei tu a dover premere {}".format(query.from_user.name))


    # check if the user is in chat_data (i.e. he is expected to answer)
    elif query.from_user.id in context.user_data:
        # check if the user is answering to his own question
        if context.user_data[query.from_user.id] == context.chat_data[query.message.message_id]['question_key']:
            # send selected answer
            msg1 = await context.bot.edit_message_text(text="Hai hai scelto: {}".format(query.data),
                                        chat_id=query.message.chat_id,
                                        message_id=query.message.message_id)

            # check correctness
            if query.data == right_answer[context.chat_data[query.message.message_id]['question_id']]:
                msg2 = await context.bot.send_message(chat_id=query.message.chat_id,
                                        text="Risposta corretta!")
                await context.bot.send_message(chat_id=query.message.chat_id,
                                        text="Benvenuto {username} e buona permanenza nel gruppo!".format(
                                            username=query.from_user.name))
                # restore standard permissions
                await context.bot.restrict_chat_member(chat_id=query.message.chat_id, user_id=query.from_user.id,
                                            permissions=standard_permissions)
                
                # delete history
                await context.bot.delete_message(chat_id=query.message.chat_id,
                                        message_id=context.chat_data[query.message.message_id]['to_be_deleted'][0])
                await context.bot.delete_message(chat_id=query.message.chat_id,
                                        message_id=context.chat_data[query.message.message_id]['to_be_deleted'][1])
                
                # clean chat after 15 sec
                async def delayed_rm(context, query=query):
                    await context.bot.delete_message(chat_id=query.message.chat_id,
                                        message_id=msg1.message_id)
                    await context.bot.delete_message(chat_id=query.message.chat_id,
                                        message_id=msg2.message_id)
                
                context.job_queue.run_once(delayed_rm, 15)
                

            else:
                msg = "Risposta errata! Entro 15 secondi sarai rimosso dal gruppo.\n"
                msg += "Rientra quando vuoi ma dovrai rispondere correttamente per poter rimanere."
                msg2 = await context.bot.send_message(chat_id=query.message.chat_id, text=msg)

                # delete history
                await context.bot.delete_message(chat_id=query.message.chat_id,
                                        message_id=context.chat_data[query.message.message_id]['to_be_deleted'][0])
                await context.bot.delete_message(chat_id=query.message.chat_id,
                                        message_id=context.chat_data[query.message.message_id]['to_be_deleted'][1])

                # kick the user after a given delay and clean the chat
                async def delayed_kick(context, query=query):
                    await context.bot.delete_message(chat_id=query.message.chat_id,
                                        message_id=msg1.message_id)
                    await context.bot.delete_message(chat_id=query.message.chat_id,
                                        message_id=msg2.message_id)
                    await context.bot.ban_chat_member(chat_id=query.message.chat_id, user_id=query.from_user.id)
                    await asyncio.sleep(2)
                    await context.bot.unban_chat_member(chat_id=query.message.chat_id, user_id=query.from_user.id)

                context.job_queue.run_once(delayed_kick, 15)

            del context.chat_data[query.message.message_id]
            del context.user_data[query.from_user.id]

        else:
            msg = "{username} questa non è la tua domanda.".format(username=query.from_user.name)
            msg = await context.bot.send_message(chat_id=query.message.chat_id, text=msg)

            # clean chat after 15 sec
            async def delayed_rm(context, query=query):
                await context.bot.delete_message(chat_id=query.message.chat_id,
                                        message_id=msg.message_id)
                
            context.job_queue.run_once(delayed_rm, 15)

    else:
        msg = "{username} tu hai già risposto.".format(username=query.from_user.name)
        msg = await context.bot.send_message(chat_id=query.message.chat_id, text=msg)

        # clean chat after 15 sec
        async def delayed_rm(context, query=query):
            await context.bot.delete_message(chat_id=query.message.chat_id,
                                    message_id=msg.message_id)
    
        context.job_queue.run_once(delayed_rm, 15)