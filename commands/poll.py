from util.decorators import restricted


@restricted
def execute(update, context):
    """
    'poll' create a new poll

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    msg = update.message.text.replace('/poll ', '').split(";")
    question = msg[0]
    options = msg[1:]
    context.bot.send_poll(chat_id=update.message.chat_id,
                          question=question,
                          options=options,
                          disable_notification=False)

    # remove command
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
