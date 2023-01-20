from util.decorators import restricted


@restricted
async def execute(update, context):
    """
    'send' send a file

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    filename = update.message.text.replace("/send_file","")
    filename = filename.strip()

    # send file
    await context.bot.send_document(chat_id=update.message.chat_id, document=open('resources/' + filename, 'rb'))
    # remove command
    await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)