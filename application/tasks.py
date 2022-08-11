from application.workers import celery
from datetime import datetime
from celery.schedules import crontab


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(1, daily_reminder.s(), name='at every second.')

@celery.task()
def daily_reminder():
    from application.misc import mailing_list, send_daily_reminder
    user_list = list(set(mailing_list()))
    print(user_list)
    now = datetime.now()
    present_time = now.strftime("%-H%-M%-S")

    # present_time = datetime(2020, 5, 17, 17)
    # print(present_time.strftime("%-H%-M%-S"))
    if present_time == '20370':
        print('Sending email................')
        send_daily_reminder(user_list)

@celery.task()
def generate_report(usr_name,n_decks,flag):
    print('Inside Tasks')
    from flask import render_template, redirect
    from application.misc import email_report
    from application.models import User,Decks,Cards
    grps = Decks.query.filter(Decks.owner.any(username=usr_name)).all()
    email_report(all_decks=grps, username=usr_name, n=n_decks, flag=flag)
