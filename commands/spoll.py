from util.decorators import restricted
from telegram import Poll
import datetime


@restricted
async def execute(update, context):
    """
    'spoll' schedule a new poll

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    if update.message.text.strip() == "/spoll":
        msg = "These are examples of scheduled POLL. Use the command followed by any of these examples.\n\n"
        msg += "Regular - anonymous:\n"
        await context.bot.send_message(chat_id=update.message.chat_id,
                                 text=msg,
                                 disable_web_page_preview=True)

        msg = "#Q: How many hours in a year?\n"
        msg += "#O: 100\n"
        msg += "#O: 876\n"
        msg += "#O: 8760\n"
        msg += "#O: 87600\n"
        msg += "#D: 1-9-2020\n"
        msg += "#H: 16:15\n\n"
        await context.bot.send_message(chat_id=update.message.chat_id,
                                 text=msg,
                                 disable_web_page_preview=True)

        msg = "Regular - not anonymous:\n"
        await context.bot.send_message(chat_id=update.message.chat_id,
                                 text=msg,
                                 disable_web_page_preview=True)

        msg = "#Q: How many hours in a year?\n"
        msg += "#O: 100\n"
        msg += "#O: 876\n"
        msg += "#O: 8760\n"
        msg += "#O: 87600\n"
        msg += "#A: 0\n"
        msg += "#D: 1-9-2020\n"
        msg += "#H: 16:15\n\n"
        await context.bot.send_message(chat_id=update.message.chat_id,
                                 text=msg,
                                 disable_web_page_preview=True)

        msg = "Quiz - anonymous:\n"
        await context.bot.send_message(chat_id=update.message.chat_id,
                                 text=msg,
                                 disable_web_page_preview=True)
        msg = "#Q: How many hours in a year?\n"
        msg += "#O: 100\n"
        msg += "#O: 876\n"
        msg += "#O: 8760\n"
        msg += "#O: 87600\n"
        msg += "#R: 2 (0-based)\n"
        msg += "#A: 1\n"
        msg += "#T: quiz\n"
        msg += "#D: 1-9-2020\n"
        msg += "#H: 16:15\n\n"
        await context.bot.send_message(chat_id=update.message.chat_id,
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
            elif "#D:" in line.upper():
                date_string = line.replace("#D:", "").replace("#d:", "").strip()
                date = [int(k) for k in date_string.split("-")]
            elif "#H:" in line.upper():
                time_string = line.replace("#H:", "").replace("#h:", "").strip()
                time = [int(k) for k in time_string.split(":")]

        async def poll_now(context, update=update):
            msg_poll = await context.bot.send_poll(chat_id=update.message.chat_id,
                                             question=question,
                                             options=options,
                                             disable_notification=False,
                                             type=poll_type,
                                             is_anonymous=anonymity,
                                             correct_option_id=correct_option)

            await context.bot.pin_chat_message(chat_id=update.message.chat_id, message_id=msg_poll.message_id,
                                         disable_notification=False)

        time = datetime.datetime(date[2], date[1], date[0], time[0], time[1], 0, 0)
        print(time)
        name = date_string + " " + time_string
        context.job_queue.run_once(poll_now, time - datetime.datetime.now(), name=name)

    # remove command
    await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
