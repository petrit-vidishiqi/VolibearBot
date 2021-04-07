import os
from discord.ext import commands
from dotenv import load_dotenv
import riot
import toornament


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


@bot.command(name='gameinfo', help = 'Checks if a given summoner is in game and shows the participating players.')
async def gameinfo(ctx, *args):

    #joining of args necessary because a summoner can consist of multiple words
    await ctx.send(riot.gameinfo(" ".join(args[:])))

@bot.command(name='nextMatch', help = 'Fetches information about the next opponent in a given toornament for a given team name')
async def nextMatch(ctx, *args):

    #joining of args for the team necessary because a team name can consist of multiple words
    print(args[0], " ".join(args[1:]))
    await ctx.send(toornament.upcoming_match_opponent(args[0], (" ".join(args[1:]))))

@bot.command(name='roster', help = 'Returns an overview of the roster for a given team in a given tournament')
async def roster(ctx, *args):

    #joining of args for the team necessary because a team name can consist of multiple words 
    print(args[0], " ".join(args[1:]))
    await ctx.send(toornament.roster(args[0], ("".join(args[1:]))))

@bot.command(name='standings', help = 'Returns the current group standings for a given team.')
async def standings(ctx, *args):

    #joining of args for the team necessary because a team name can consist of multiple words 
    print(args[0], " ".join(args[1:]))
    await ctx.send(toornament.standings(args[0], ("".join(args[1:]))))



bot.run(TOKEN)
