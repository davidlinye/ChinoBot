import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_SERVER')

client = discord.Client()

bot = commands.Bot(command_prefix='?')

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def addCounter(filename):
    filetest = open(filename,'a+')
    filetest.close()
    with open(filename, 'r+') as lines:
        countstring = lines.read()
        filter(lambda x: x.isdigit(), countstring)
        if not hasNumbers(countstring):
            countstring = "0"
        count = int(countstring, base=10)
        count = count + 1
    with open(filename, 'w') as lines:
        countstring = str(count)
        lines.write(countstring)

@client.event
async def on_message(message):
    response = message.content.lower() + ' count: '
    if message.author == client.user:
        return
    if message.content.lower() == 'im the biggest nozomi fan' or message.content.lower() == 'i\'m the biggest nozomi fan':
        addCounter('fan.txt')
        response = response + open('fan.txt', 'r').read()
        await message.channel.send(response)
    if message.content.lower() == 'uwu':
        addCounter('uwu.txt')
        response = response + open('uwu.txt', 'r').read()
        await message.channel.send(response)
    if message.content.lower() == 'owo':
        addCounter('owo.txt')
        response = response + open('owo.txt', 'r').read()
        await message.channel.send(response)

#@bot.command(name='addCounter')
#async def newCounter(letext):
#    if 

client.run(TOKEN)
