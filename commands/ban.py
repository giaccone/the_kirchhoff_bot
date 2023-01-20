from util.decorators import restricted


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