from util.decorators import restricted


@restricted
def execute(update, context):
    """
    'cg' (clean group) remove inactive users

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    for member in context.chat_data:
        context.bot.kickChatMember(chat_id=update.message.chat_id, user_id=member)
        context.bot.unbanChatMember(chat_id=update.message.chat_id, user_id=member)

    # remove command
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)