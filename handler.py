import imp
from multiprocessing import context
import os

import discord

from discord.ext import commands
from dotenv import load_dotenv

import asyncio

import time
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

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

#sends reminder
def send_reminder(reminder):
    print(reminder)
    return reminder

#adds reminder to scheduler
def create_reminder(what, who, when):
    time_to_remind = str_to_datetime(when)
    reminder = who + ': ' + '\"' + what + '\"'
    scheduler.add_job(send_reminder, 'date', run_date=time_to_remind, args=[reminder])

@bot.command(name='test')
async def set_reminder(ctx):

    def check(m):
        return m.content != 'quit'

    await ctx.send("Who am I reminding?")
    
    who = await bot.wait_for('message', check=check)
    await ctx.send('Okay')
    await ctx.send(who.content)

    await ctx.send("What am I reminding them about?")
    
    what = await bot.wait_for('message', check=check)
    await ctx.send('Okay')
    await ctx.send(what.content)

    await ctx.send("When should I remind them? (Please respond in the format of this example: 12:34 PM 5/6/22)")
    
    when = await bot.wait_for('message', check=check)
    await ctx.send('Okay')
    await ctx.send(when.content)
   


bot.run(TOKEN)
