from telegram.constants import ParseMode
from util.decorators import restricted
from configparser import ConfigParser
import asyncio
import logging

# setup logger
logger = logging.getLogger(__name__)


@restricted
async def execute(update, context):
    """
    'test' activate/deactivate the captcha for new users

    :param update: bot update
    :param context: context
    :return: None
    """
    config = ConfigParser()
    config.read('variable_config.ini')
    chat_title = update.message.chat.title
    chat_id = update.message.chat_id

    if config['entry_test']['active'] == 'True':
        config['entry_test']['active'] = 'False'
        sent_message = await context.bot.send_message(chat_id=update.message.chat_id,
                             text="Captcha disabilitato",
                             parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        
        logger.info("Captcha disabilitato - chat: {} - chat_id:{}".format(chat_title, chat_id))
        
    elif config['entry_test']['active'] == 'False':
        config['entry_test']['active'] = 'True'
        sent_message = await context.bot.send_message(chat_id=update.message.chat_id,
                             text="Captcha abilitato",
                             parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        
        logger.info("Captcha abilitato - chat: {} - chat_id:{}".format(chat_title, chat_id))
    
    with open('variable_config.ini', 'w') as configfile:
        config.write(configfile)
    
    await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
    await asyncio.sleep(5)
    await context.bot.delete_message(chat_id=update.message.chat_id, message_id=sent_message.message_id)