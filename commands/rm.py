from util.decorators import restricted
from telegram.error import TelegramError


@restricted
def execute(update, context):
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
            except TelegramError:
                c += 1

    else:
        context.bot.delete_message(chat_id=update.message.chat_id,
                                   message_id=update.message.reply_to_message.message_id)
        # remove command
        context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
