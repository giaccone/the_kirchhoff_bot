from util.decorators import restricted
import logging

# setup logger
logger = logging.getLogger(__name__)


@restricted
async def execute(update, context):
    """
    'ban' ban user out from the group

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    user_id = update.message.reply_to_message.from_user.id
    await context.bot.ban_chat_member(chat_id=update.message.chat_id, user_id=user_id)

    # remove command
    await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)

    # log
    chat_title = update.message.chat.title
    chat_id = update.message.chat_id
    first_name = update.message.reply_to_message.from_user.first_name
    username = update.message.reply_to_message.from_user.username
    logger.info("ban - chat: {} - chat_id:{} - username:{} - first_name:{} - user_id:{}".format(chat_title,
                                                                                                chat_id,
                                                                                                username,
                                                                                                first_name,
                                                                                                user_id))