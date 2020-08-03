from util.decorators import restricted


@restricted
def execute(update, context):
    """
    'job_stop' stops a job

    :param update: bot update
    :param context: CallbackContext
    :return: None
    """
    jobs = update.message.text.replace("/job_stop","")
    jobs = jobs.split(";")
    for jname in jobs:
        j = context.job_queue.get_jobs_by_name(jname.strip())
        for ele in j:
            ele.schedule_removal()