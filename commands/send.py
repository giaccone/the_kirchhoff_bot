from util.decorators import restricted
from telegram import ParseMode


@restricted
def execute(update, context):
    """
    'send' send a message in the group through the bot
    usage: /send message of the text

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    msg = update.message.text.replace('/send ','').replace('\*','*'). replace('\_','_')
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
    if update.message.reply_to_message is None:
        context.bot.send_message(chat_id=update.message.chat_id,
                                text=msg,
                                parse_mode=ParseMode.MARKDOWN,
                                disable_web_page_preview=True)
    else:
        context.bot.send_message(chat_id=update.message.chat_id,
                                text=msg,
                                parse_mode=ParseMode.MARKDOWN,
                                disable_web_page_preview=True,
                                reply_to_message_id=update.message.reply_to_message.message_id)