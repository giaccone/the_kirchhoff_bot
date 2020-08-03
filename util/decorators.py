from functools import wraps
from config import LIST_OF_ADMINS


def restricted(func):
    """
    'restricted' decorates a function so that it can be used only to allowed users

    :param func: function to be decorated
    :return: function wrapper
    """
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            print("Unauthorized access denied for {}.".format(user_id))
            context.bot.send_message(chat_id=update.message.chat_id, text="You are not authorized to run this command")
            return
        return func(update, context, *args, **kwargs)
    return wrapped
