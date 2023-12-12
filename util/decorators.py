from functools import wraps
from config import LIST_OF_ADMINS
import logging

# setup logger
logger = logging.getLogger(__name__)


def restricted(func):
    """
    'restricted' decorates a function so that it can be used only to allowed users

    :param func: function to be decorated
    :return: function wrapper
    """
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            username = "@" + update.effective_user.username \
                if update.effective_user.username is not None \
                    else update.effective_user.name
            logger.warning("ACCESS DENIEND. username: %s - id: %s - text: %s", username, user_id, update.message.text)
            await context.bot.send_message(chat_id=update.message.chat_id, text="You are not authorized to run this command")
            return
        return await func(update, context, *args, **kwargs)
    return wrapped
