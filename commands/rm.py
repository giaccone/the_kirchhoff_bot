from util.decorators import restricted
from telegram.error import TelegramError


@restricted
async def execute(update, context):
    """
    'rm' remove messages
    usage: /rm (in reply to the message to be deleted)

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """


    await context.bot.delete_message(chat_id=update.message.chat_id,
                                   message_id=update.message.reply_to_message.message_id)
    # remove command
    await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
