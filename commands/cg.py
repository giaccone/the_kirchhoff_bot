from util.decorators import restricted


@restricted
async def execute(update, context):
    """
    'cg' (clean group) remove inactive users

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    for member in context.chat_data:
        await context.bot.ban_chat_member(chat_id=update.message.chat_id, user_id=member)
        await context.bot.unban_chat_member(chat_id=update.message.chat_id, user_id=member)

    # remove command
    await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)