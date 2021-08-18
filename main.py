import discord 
import os
import random
from datetime import datetime
from pytz import timezone
from keep_alive import keep_alive
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot('.', intents=intents)

format = "%d/%m/%Y %H:%M:%S %Z%z"
now_utc = datetime.now(timezone('UTC'))
now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
dt_string = now_asia.strftime(format)
bot.remove_command('help')

@bot.event
async def on_ready():
  print('Logged in as: {0.user}'.format(bot))

@bot.event
async def on_message(message):
  id = message.guild.id
  log = ('message from {0.author}: {0.content}'.format(message))
  file1 = open(f'{id}.txt', 'a')
  file1.write('\n' + dt_string + ': ' + log)
  file1.close()
  await bot.process_commands(message)

@bot.command(pass_context=True)
async def serverid(ctx):
  id = ctx.message.guild.id
  await ctx.send(id)

@bot.command()
async def help(ctx):
  await ctx.send('```fix\nLogBot\'s main functionality is maintaining text logs of a server. It is still under development.\n\nLogbot Commands:\ntest: Check if bot is online and functioning as expected\nrp: Make LogBot repeat whatever you say\nprintlog: Print all logs maintained by LogBot (manage server perms required to run this command)\nmembers: Get a list of all server members along with their User ID in a text file (manage server perms required to run this command)\ncrystalball: ask a question and let LogBot answer```' )

@bot.command()
async def test(ctx):
  await ctx.send('LogBot is functioning normally')

@bot.command(pass_context = True)
@commands.has_permissions(manage_guild = True)
async def printlog(ctx):
  id = ctx.message.guild.id
  await ctx.send(file=discord.File(f'{id}.txt'))

@bot.command()
async def rp(ctx, *, arg):
  await ctx.send(arg)

@bot.command(pass_context = True)
@commands.has_permissions(manage_guild = True)
async def members(ctx):
    with open('users.txt','w') as f:
        async for member in ctx.guild.fetch_members(limit=None):
            print("{}, User ID: {}".format(member, member.id), file=f,)
    print("done")
    await ctx.send(file=discord.File('users.txt'))
    open('users.txt', 'w').close()

@bot.command()
async def crystalball(ctx, *, arg):
  choice = ['yes','no','maybe','for sure','um.. no?']
  await ctx.send(random.choice(choice))

keep_alive()
bot.run(os.getenv('token'))
