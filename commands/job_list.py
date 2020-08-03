from util.decorators import restricted
from telegram.error import TelegramError
from config import LIST_OF_ADMINS


@restricted
def execute(update, context):
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
        except TelegramError:
            pass

    # remove command
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
