import os
import remindario

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

remindario.start()

bot = commands.Bot(command_prefix='/')

@bot.command(name='set-reminder')
async def set_reminder(ctx):

    remindario.add_reminder()
    response = 'not here yet'
    await ctx.send(response)

bot.run(TOKEN)
