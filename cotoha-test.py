import configparser
import discord
from discord.ext import commands

import cotoha as cth
import orchid as orc

bot = commands.Bot(command_prefix='$')
client = discord.Client()
orchid = orc.Orchid()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
        
@bot.command()
async def test(ctx, arg):
    await ctx.send(orchid.get_weak_point(arg))

@bot.command()
async def waza(ctx, arg):
    await ctx.send(orchid.get_weak_point(arg))


config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')
TOKEN = config_ini['DISCORD']['Token']
bot.run(TOKEN)



