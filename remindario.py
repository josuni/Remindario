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

#helpers
def str_to_datetime(str):
    #Ex str: '12:34 PM 5/6/22'
    dt = datetime.strptime(str, '%I:%M %p %m/%d/%y')
    return dt

def dt_is_incorrect_format(message):
        try:
            str_to_datetime(message)
        except:
            print('Time is Incorrect Format')
            return True
        return False

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

#commands
@bot.command()
async def test(ctx):
    scheduler.add_job(send_reminder, args=['This is a test.'])

@bot.command(name='set-reminder-quick')
async def set_reminder(ctx, who, what, when):

    requester = ctx.message.author

    def check_author(message):
        return message.author == requester

    if dt_is_incorrect_format(when):
        await ctx.send('Hmm, something is not formatted right. Try \'set-reminder\' instead.')
    else:
        m = 'Let\'s make sure I have this right. You would like to send a message to ' + who + ' about ' + '\"' + what + '\"' + ' at ' + when + '? y/n'
        await ctx.send(m)
        response = await bot.wait_for('message', check=check_author)
        if response.content == 'y':
                create_reminder(what, who, when)
                await ctx.send('Alrighty! Reminder added.')
        else:
            await ctx.send('Reminder canceled.')


@bot.command(name='set-reminder')
async def set_reminder(ctx):

    requester = ctx.message.author

    def check_author(message):
        return message.author == requester

    await ctx.send("Who am I reminding?")
    who = await bot.wait_for('message', check=check_author)

    await ctx.send("What am I reminding them about?")
    what = await bot.wait_for('message', check=check_author)

    await ctx.send("When should I remind them? (Please respond in the format of this example: 12:34 PM 5/6/22)")  
    when = await bot.wait_for('message', check=check_author)

    while dt_is_incorrect_format(when.content):
        await ctx.send('Sorry, the time is in an incorrect format. Please try again.')
        when = await bot.wait_for('message', check=check_author)

    m = 'Let\'s make sure I have this right. You would like to send a message to ' + who.content + ' about ' + '\"' + what.content + '\"' + ' at ' + when.content + '? y/n'
    await ctx.send(m)
    response = await bot.wait_for('message', check=check_author)
    if response.content == 'y':
            create_reminder(what.content, who.content, when.content)
            await ctx.send('Alrighty! Reminder added.')
    else:
        await ctx.send('Reminder canceled.')
   


bot.run(TOKEN)
