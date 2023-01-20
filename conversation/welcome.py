from telegram import InlineKeyboardMarkup
from util.permission import initial_permission
from random import randrange
from util.question_database import question, answer
import uuid
import time
from configparser import ConfigParser
import asyncio


async def execute(update, context):
    """
    'welcome_message' generated the message sent to new users joining the group

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    config = ConfigParser()
    config.read('variable_config.ini')

    if config['entry_test']['active'] == 'True':
        # welcome message
        for member in update.message.new_chat_members:
            msg = ""
            if member.username is None:
                msg += "Benvenuto {name}. Per prima cosa imposta uno username ".format(name=member.name)
                msg += "per facilitare le conversazioni future, grazie.\n\n"
                msg += "Inoltre, per poter rimanere dovrai rispondere correttamente alla seguente domanda.\n"
                msg += "(Se sbagli sarai rimosso dal gruppo con possibilità di rientrare quando vuoi)."
                context.chat_data[member.id] = 0
            else:
                msg += "Ciao {username}!\n".format(username=member.username)
                msg += "Benvenuto nel gruppo. Per poter rimanere dovrai rispondere alla seguente domanda.\n"
                msg += "(Se sbagli sarai rimosso dal gruppo con possibilità di rientrare quando vuoi)."
            await update.message.reply_text(msg)

            # update chat_data with the used_id and the index of its question
            # pick a random question
            question_id = randrange(len(question))
            # remove permissions
            await context.bot.restrict_chat_member(chat_id=update.message.chat_id, user_id=member.id,
                                        permissions=initial_permission)

            # send the question
            question_text = "{name}\n".format(name=member.name) + question[question_id]
            possible_answers = answer[question_id]
            reply_markup = InlineKeyboardMarkup(possible_answers)
            time.sleep(0.5)
            await context.bot.send_message(chat_id=update.message.chat_id, text=question_text, reply_markup=reply_markup)

            # generate a random key
            key = str(uuid.uuid4())
            # get the message_id of the InlineKeyboardMarkup
            message_id = update.message.message_id + 2
            # bind InlineKeyboard to user by means of chat_data and user_data
            context.chat_data[message_id] = dict()
            context.chat_data[message_id]['question_key'] = key
            context.chat_data[message_id]['question_id'] = question_id
            context.chat_data[message_id]['to_be_deleted'] = [update.message.message_id, update.message.message_id + 1]
            context.user_data[member.id] = key
        
    elif config['entry_test']['active'] == 'False':
        for member in update.message.new_chat_members:
            msg = ""
            if member.username is None:
                msg += "Benvenuto {name}. Per favore imposta uno username ".format(name=member.name)
                msg += "per facilitare le conversazioni future, grazie.\n\n"
                context.chat_data[member.id] = 0
            else:
                msg += "Ciao {username}!\n".format(username=member.username)
                msg += "Benvenuto nel gruppo."
            sent_message = await update.message.reply_text(msg)
            await asyncio.sleep(10)
            await context.bot.delete_message(chat_id=update.message.chat_id, message_id=sent_message.message_id)


