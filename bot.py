import os
from discord.ext import commands
from dotenv import load_dotenv
import riot


'''
This is the entry point of the Discord Bot
Here the token of the Bot gets passed to the script and the Bot gets started.
Every available command is defined below and corresponds to functions, 
that will be defined elsewhere.
'''


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='/')


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command(name='gameinfo')
async def gameinfo(ctx, *args):

    #joining of args necessary because a summoner can consist of multiple words
    await ctx.send(riot.gameinfo(" ".join(args[:])))


bot.run(TOKEN)