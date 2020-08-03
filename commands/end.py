from util.decorators import restricted


@restricted
def execute(update, context):
    """
    'end' close an existing poll

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    context.bot.stop_poll(chat_id=update.message.chat_id, message_id=update.message.reply_to_message.message_id)

    # remove command
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)