from multiprocessing import context
import os

import discord

from discord.ext import commands
from dotenv import load_dotenv

from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = os.getenv('REMINDER_CHANNEL')

scheduler = AsyncIOScheduler()

bot = commands.Bot(command_prefix='/')

@bot.event
async def on_ready():
    print("Starting...")
    scheduler.start()

#helper
def str_to_datetime(str):
    #Ex str: '12:34 PM 5/6/22'
    dt = datetime.strptime(str, '%I:%M %p %m/%d/%y')
    return dt

#adds reminder to scheduler
def create_reminder(what, who, when):
    time_to_remind = str_to_datetime(when)
    reminder = who + ': ' + '\"' + what + '\"'
    scheduler.add_job(send_reminder, 'date', run_date=time_to_remind, args=[reminder])

#sends reminder
async def send_reminder(reminder):
    print(reminder)
    channel = discord.utils.get(bot.get_all_channels(), name=CHANNEL)
    await channel.send(reminder)

@bot.command(name='test')
async def test(ctx):
    scheduler.add_job(send_reminder, args=['This is a test.'])

@bot.command(name='set-reminder')
async def set_reminder(ctx):

    def check(message):
        return message.content != 'quit'

    await ctx.send("Who am I reminding?")
    who = await bot.wait_for('message', check=check)

    await ctx.send("What am I reminding them about?")
    what = await bot.wait_for('message', check=check)

    await ctx.send("When should I remind them? (Please respond in the format of this example: 12:34 PM 5/6/22)")  
    when = await bot.wait_for('message', check=check)

    create_reminder(what.content, who.content, when.content)
    await ctx.send('Reminder added.')
   


bot.run(TOKEN)
