from util.decorators import restricted


@restricted
def execute(update, context):
    """
    'pin' pin a message

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """

    # pin message
    context.bot.pin_chat_message(chat_id=update.message.chat_id, message_id=update.message.reply_to_message.message_id,
                                 disable_notification=False)

    # remove command
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)