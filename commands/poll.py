from util.decorators import restricted
from telegram import Poll


@restricted
def execute(update, context):
    """
    'poll' create a new poll

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    if update.message.text.strip() == "/poll":
        msg = "These are examples of POLL. Use the command followed by any of these examples.\n\n"
        msg += "Regular - anonymous:\n"
        msg += "--------------------\n"
        msg += "#Q: How many hours in a year?\n"
        msg += "#O: 100\n"
        msg += "#O: 876\n"
        msg += "#O: 8760\n"
        msg += "#O: 87600\n\n"
        msg += "Regular - not anonymous:\n"
        msg += "--------------------\n"
        msg += "#Q: How many hours in a year?\n"
        msg += "#O: 100\n"
        msg += "#O: 876\n"
        msg += "#O: 8760\n"
        msg += "#O: 87600\n"
        msg += "#A: 0\n\n"
        msg += "Quiz - anonymous:\n"
        msg += "-----------------\n"
        msg += "#Q: How many hours in a year?\n"
        msg += "#O: 100\n"
        msg += "#O: 876\n"
        msg += "#O: 8760\n"
        msg += "#O: 87600\n"
        msg += "#R: 2 (0-based)\n"
        msg += "#A: 1\n"
        msg += "#T: quiz\n"
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=msg,
                                 disable_web_page_preview=True)
    else:
        # defaults
        poll_type = Poll.REGULAR
        anonymity = True
        correct_option = None
        # remove command
        msg = update.message.text.replace('/poll ', '').split("\n")
        # get question and options
        options = []
        for line in msg:
            if "#Q:" in line.upper():
                question = line.replace("#Q:", "").replace("#q:", "").strip()
            elif "#O:" in line.upper():
                options.append(line.replace("#O:", "").replace("#o:", "").strip())
            elif "#A:" in line.upper():
                anonymity = bool(int(line.replace("#A:", "").replace("#a:", "").strip()))
            elif "#T:" in line.upper():
                flag = line.replace("#T:", "").replace("#t:", "").strip().lower()
                if flag == 'quiz':
                    poll_type = Poll.QUIZ
                elif flag == 'regular':
                    poll_type = Poll.REGULAR
            elif "#R:" in line.upper():
                correct_option = int(line.replace("#R:", "").replace("#r:", "").strip())

        context.bot.send_poll(chat_id=update.message.chat_id,
                              question=question,
                              options=options,
                              disable_notification=False,
                              type=poll_type,
                              is_anonymous=anonymity,
                              correct_option_id=correct_option)

    # remove command
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
