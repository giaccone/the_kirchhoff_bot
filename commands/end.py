from util.decorators import restricted


@restricted
async def execute(update, context):
    """
    'end' close an existing poll

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    await context.bot.stop_poll(chat_id=update.message.chat_id, message_id=update.message.reply_to_message.message_id)

    # remove command
    await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)