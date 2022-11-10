from util.decorators import restricted
from telegram import ParseMode


@restricted
def execute(update, context):
    """
    'send_imahe' send an image
    usage: /send_image

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
    context.bot.send_photo(chat_id=update.message.chat_id, photo=open('./resources/immagine.png', 'rb'))