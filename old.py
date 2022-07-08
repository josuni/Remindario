import time
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler


scheduler = AsyncIOScheduler()

def start():
    scheduler.start()

def str_to_datetime(str):
    #Ex str: '12:34 PM 5/6/22'
    dt = datetime.strptime(str, '%I:%M %p %m/%d/%y')
    return dt

def create_reminder(what, who, when):
    time_to_remind = str_to_datetime(when)
    reminder = who + ': ' + '\"' + what + '\"'
    scheduler.add_job(send_reminder, 'date', run_date=time_to_remind, args=[reminder])
    


