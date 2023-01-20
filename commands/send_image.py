from util.decorators import restricted


@restricted
async def execute(update, context):
    """
    'send_imahe' send an image
    usage: /send_image filename (without extension)

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    filename = update.message.text.replace("/send_image","").strip()
    filename = filename.strip()

    await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
    await context.bot.send_photo(chat_id=update.message.chat_id, photo=open('./resources/' + filename + '.png', 'rb'))