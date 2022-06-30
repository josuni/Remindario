import os

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='/')

@bot.command(name='set-reminder')
async def set_reminder(ctx):

    response = "Hello Again"
    await ctx.send(response)

bot.run(TOKEN)
