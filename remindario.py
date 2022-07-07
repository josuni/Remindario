import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler


sched = BackgroundScheduler()

def str_to_datetime(str):
    #Ex str: '12:34 PM 5/6/22'
    dt = datetime.strptime(str, '%I:%M %p %m/%d/%y')
    return dt

def reminder(str):
    print(str)

def add_reminder():
    sched.add_job(reminder, args=['Remind'])

def start():
    sched.add_job(reminder, args=['Sleep'])
    sched.start()
