from util.decorators import restricted
import datetime


@restricted
def execute(update, context):
    """
    'spoll' schedule a new poll

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    poll_data, date_name = update.message.text.split('_end_')
    date, name = date_name.split('_name_')
    msg = poll_data.replace('/spoll ', '').split(";")
    date = [int(k) for k in date.split(";")]

    question = msg[0]
    options = msg[1:]

    def poll_now(context, update=update):
        msg_poll = context.bot.send_poll(chat_id=update.message.chat_id,
                                         question=question,
                                         options=options,
                                         disable_notification=False)

        context.bot.pin_chat_message(chat_id=update.message.chat_id, message_id=msg_poll.message_id,
                                     disable_notification=False)

    time = datetime.datetime(date[0], date[1], date[2], date[3], date[4], 0, 0)
    context.job_queue.run_once(poll_now, time, name=name)

    # remove command
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
