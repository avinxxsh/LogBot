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

class OwnerCommands(commands.Cog):

    def __init__(self, bot):
        self.client = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("OwnerCommands Is Ready")

    @commands.command()
    async def servers(self, ctx):
        activeservers = bot.guilds
        for guild in activeservers:
            await ctx.send(guild.name)
            print(guild.name)

def setup(bot):
    bot.add_cog(OwnerCommands(bot))

    
@bot.event
async def on_ready():
  print('Logged in as: {0.user}'.format(bot))
#discord.TextChannel.name

@bot.event
async def on_message(message):
  id = message.guild.id
  #IST = pytz.timezone('Asia/Kolkata')
  #datetime_ist = datetime.now(IST)
  ts = time.time()
  st = datetime.datetime.fromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S GMT+00:00')
  log = ('message from {0.author}: {0.content} (in channel:'.format(message) + f' {message.channel.name})')
  file1 = open(f'{id}.txt', 'a')
  file1.write('\n' + st + ': ' + log)
  file1.close()
  await bot.process_commands(message)
  
  #bot replies to mentions
  if bot.user.mentioned_in(message):
    await message.channel.send('```yaml\ntype \".help\" for more information```')
  
  #if message.content =='.testid':
  #  id = message.guild.id
  #  print(id)
    

@bot.command(pass_context=True)
async def serverid(ctx):
  id = ctx.message.guild.id
  await ctx.send(id)

@bot.command()
async def help(ctx):
  await ctx.send('```yaml\nLogBot\'s main functionality is maintaining text logs of a server. It is still under development. [prefix is \'.\' by default]\n\nLogbot Commands:\nUtility:\n- test: Check if bot is online and functioning as expected\n- printlog: Print all logs maintained by LogBot (manage server perms required to run this command)\n- clearlog: Clear all logs maintained by LogBot (administrator perms required to run this command)\n- members: Get a list of all server members along with their User ID in a text file (manage server perms required to run this command)\n- serverid: Get the ID of current Guild/Server\n- update: Get information on the last LogBot update and it\'s features\n\nMisc:\n- rp: Make LogBot repeat whatever you say\n- crystalball: ask a yes/no question and let LogBot answer```' )

@bot.command()
async def update(ctx):
  await ctx.send('```yaml\nLogBot Version: Stable.v6.1\n\nLast Added Features:\n- clearlog command can be run by admins to clear all logs stored by LogBot\n- LogBot Stable.v5 onwards: When LogBot is removed from a server all log files of server are automatically deleted\n- Channel Names: Logs now mention the channel in which a message was sent in\n-.help Updated .help command ```')

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
    message = f'```ERROR: {error}```'
  await ctx.send(message)

@bot.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def clearlog(ctx):
  id = ctx.message.guild.id
  open(f'{id}.txt', 'w').close()
  await ctx.send('```SUCCESS: Log Cleared```')


@clearlog.error
async def error_clearlog(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    message = f'```ERROR: {error}```'
  else:
    message = f'```ERROR: {error}```'
  await ctx.send(message)

@bot.event
async def on_guild_remove(guild): #delete logs when leave/removed from server
  id = guild.id
  os.remove(f'{id}.txt')
  print('Log File Removed')
  await bot.process_commands(guild)
  
@bot.command()
async def rp(ctx, *, arg):
  await ctx.send(arg)

@bot.command(pass_context = True)
@commands.has_permissions(manage_guild = True)
async def members(ctx):
    with open('users.txt','w') as f:
        async for member in ctx.guild.fetch_members(limit=None):
            print("{}, User ID: {}".format(member, member.id), file=f,)
    print('Members and ID\'s Printed')
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

#@bot.command()
#async def servercount(ctx):
#  guilds = list(self.client.guilds)
    
@bot.command()
async def crystalball(ctx, *, arg):
  choice = ['yes','no','maybe','for sure','um.. no?']
  await ctx.send(random.choice(choice))

@crystalball.error
async def error_cb(ctx, error):
  message = f'```yaml\nERROR: {error}```'
  await ctx.send(message)

@bot.command()
async def vote(ctx):
  await ctx.send('Vote for LogBot at: https://top.gg/bot/877517529520668702/vote/')

keep_alive()
bot.run(os.getenv('token'))
