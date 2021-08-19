import discord 
import os
import random
import datetime
import time
#import pytz
from keep_alive import keep_alive
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot('.', intents=intents)

bot.remove_command('help')

@bot.event
async def on_ready():
  print('Logged in as: {0.user}'.format(bot))

@bot.event
async def on_message(message):
  id = message.guild.id
  #IST = pytz.timezone('Asia/Kolkata')
  #datetime_ist = datetime.now(IST)
  ts = time.time()
  st = datetime.datetime.fromtimestamp(ts).strftime('%d/%m-%Y %H:%M:%S GMT+00:00')
  log = ('message from {0.author}: {0.content}'.format(message))
  file1 = open(f'{id}.txt', 'a')
  file1.write('\n' + st + ': ' + log)
  file1.close()
  await bot.process_commands(message)

@bot.command(pass_context=True)
async def serverid(ctx):
  id = ctx.message.guild.id
  await ctx.send(id)

@bot.command()
async def help(ctx):
  await ctx.send('```fix\nLogBot\'s main functionality is maintaining text logs of a server. It is still under development.\n\nLogbot Commands:\n- test: Check if bot is online and functioning as expected\n- rp: Make LogBot repeat whatever you say\n- printlog: Print all logs maintained by LogBot (manage server perms required to run this command)\n- members: Get a list of all server members along with their User ID in a text file (manage server perms required to run this command)\n- serverid: Get the ID of current Guild/Server\n- crystalball: ask a question and let LogBot answer```' )

@bot.command()
async def test(ctx):
  await ctx.send('LogBot is functioning normally')

@bot.command(pass_context = True)
@commands.has_permissions(manage_guild = True)
async def printlog(ctx):
  id = ctx.message.guild.id
  await ctx.send(file=discord.File(f'{id}.txt'))

@printlog.error
async def error_printlog(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    message = f'```ERROR:  {error}```'
  else:
    message = '```Unexpected Error Encountered!```'
  await ctx.send(message)

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

@members.error
async def error_members(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    message = f'```ERROR: {error}```'
  else:
    message = '```Unexpected Error Encountered!```'
  await ctx.send(message)
#@bot.command()
#async def channels(ctx):
 # channel_list = []
  #id = ctx.message.guild.id
  #for guild in ctx.bot.guilds:
   # if discord.Guild.id == id:
    #  for channel in guild.channels:
     #   if ctx.guild.id == id:
      #    channel_list.append(bot.Guildchannel.name)
       # else:
        #  await ctx.send('```An Unexpected ERROR Occurred```')
  #await ctx.send(channel_list)

@bot.command()
async def ping(ctx):
    await ctx.send('Pong! **{0}ms**'.format(round(bot.latency * 1000, 1)))
    
@bot.command()
async def crystalball(ctx, *, arg):
  choice = ['yes','no','maybe','for sure','um.. no?']
  await ctx.send(random.choice(choice))

keep_alive()
bot.run(os.getenv('token'))
