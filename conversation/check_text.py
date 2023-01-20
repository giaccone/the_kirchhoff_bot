from telegram.constants import ParseMode
from configparser import ConfigParser


async def execute(update, context):
    """
    'check_text' reply to selected text messages
    * warn users without username
    * warn users using incorrect terminology

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """

    # check presenza of hot words
    if 'voltaggio' in update.message.text.lower():
        msg = "Il termine voltaggio, sebbene sia largamente utilizzato *è scorretto*. Ti vieto di utilizzarlo!"
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
        await context.bot.send_photo(chat_id=update.message.chat_id, photo=open('./resources/voltaggio.png', 'rb'))
    
    # detect macro
    if update.message.text.lower().strip()[0] == '!':
        config = ConfigParser()
        config.read('config.ini')
        key = update.message.text.lower().strip()[1:]
        
        # check if the marco is in the ini file
        if key in config:
            # check if it is a meme
            if 'path' in config[key]: 
                path = config[key]['path'].replace('"','')
                msg = config[key]['msg'].replace('"','')
                await context.bot.send_photo(chat_id=update.message.chat_id, photo=open(path, 'rb'))
                await context.bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=ParseMode.MARKDOWN)
            # otherwise it is another command
            else:
                msg = config[key]['msg'].replace('"','')
                await context.bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=ParseMode.MARKDOWN)

        # other hardcoded commands
        elif key == 'list':
            msg = 'List of available macro:\n'
            for element in config:
                if 'path' in config[element]:
                    msg += f"  (meme)    !{element}\n"
                else:
                    if element != 'DEFAULT':
                        msg += f"  !{element}\n"

            await context.bot.send_message(chat_id=update.message.chat_id, text=msg)
               
        else:
            msg = "la macro *!{}* non è registrata".format(key)
            await context.bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=ParseMode.MARKDOWN)
        
        del config
