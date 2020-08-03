from util.decorators import restricted


@restricted
def execute(update, context):
    """
    'ban' ban user out from the group

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    user_id = update.message.reply_to_message.from_user.id
    context.bot.kickChatMember(chat_id=update.message.chat_id, user_id=user_id)