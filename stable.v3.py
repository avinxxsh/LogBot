import discord 
import os
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
  log = ('message from {0.author}: {0.content}'.format(message))
  file1 = open('log.txt', 'a')
  file1.write('\n' + dt_string + ': ' + log)
  file1.close()
  await bot.process_commands(message)

@bot.command()
async def help(ctx):
  await ctx.send('LogBot\'s main functionality is maintaining text logs of a server. It is still under development.\n\n**Logbot Commands:**\n**test**: Check if bot is online and functioning as expected\n**rp**: Make LogBot repeat whatever you say\n**printlog**: Print all logs maintained by LogBot *(note that only admins can run this command)*' )

@bot.command()
async def test(ctx):
  await ctx.send('bot functionality is normal')

@bot.command(pass_context = True)
@commands.has_permissions(manage_guild = True)
async def printlog(ctx):
 await ctx.send(file=discord.File('log.txt'))

@bot.command()
async def rp(ctx, *, arg):
  await ctx.send(arg)

@bot.command()
async def members(ctx):
    with open('users.txt','w') as f:
        async for member in ctx.guild.fetch_members(limit=None):
            print("{}, User ID: {}".format(member, member.id), file=f,)
    print("done")
    await ctx.send(file=discord.File('users.txt'))
    open('users.txt', 'w').close()




keep_alive()
bot.run(os.getenv('token'))
