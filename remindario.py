import time
from datetime import datetime
from apscheduler.schedulers.background import BlockingScheduler

def str_to_datetime(str):
    #Ex str: '11:15 PM 7/12/22'
    dt = datetime.strptime(str, '%I:%M %p %m/%d/%y')
    return dt

print(str_to_datetime('11:15 PM 7/12/22'))


def event():
    print('EVENT')

#scheduler = BlockingScheduler()

#scheduler.add_job(event, 'date', run_date=time_requested)

#scheduler.start()

def message():
    message = 'wassup'
    return message