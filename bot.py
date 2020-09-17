import os
import random
import sqlite3
import discord
import db

from db import DB
from sqlite3 import Error
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_SERVER')
OWNER = os.getenv('DISCORD_OWNER')

client = discord.Client()

bot = commands.Bot(command_prefix='?', owner_id=int(OWNER))

dbfilelocation = "./wordcount.db"

def create_connection(dbfilename):
    conn = None
    try:
        conn = sqlite3.connect(dbfilename)
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn

dbconn = create_connection(dbfilelocation)

@bot.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print("on_ready")
    #print(
    #    f'{client.user} is connected to the following guild:\n'
    #    f'{guild.name}(id: {guild.id})'
    #)
    cur = dbconn.cursor()
    createtable = \
    "CREATE TABLE wordcount (id integer PRIMARY KEY, TEXT text DEFAULT NULL, COUNT integer DEFAULT 0)"
    try:
        cur.execute(createtable)
    except Error as e:
        print(e)

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def addCountercheck(filename):
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

def filterNumbers(string):
    tempstring = ""
    for char in string:
        if char.isdigit():
            tempstring = tempstring + char
    return tempstring

@bot.event
async def on_message(message):
    response = message.content.lower() + ' count: '
    cur = None
    print("on_message respond code")
    if message.author == client.user:
        return
    cur = dbconn.cursor()
    tempstring = message.content.lower()
    cur.execute("SELECT * FROM wordcount WHERE LOWER(TEXT)=?", (tempstring,))
    rows = cur.fetchall()
    print(rows)
    if rows:
        print("in rows")
        cur.execute("UPDATE wordcount SET COUNT = COUNT + 1 WHERE LOWER(TEXT)=?", (tempstring,))
        dbconn.commit()
        cur.execute("SELECT COUNT FROM wordcount WHERE LOWER(TEXT)=?", (tempstring,))
        rows = cur.fetchall()
        temprows = str(rows[0])
        temprows = filterNumbers(temprows)
        response = response + temprows
        await message.channel.send(response)
    await bot.process_commands(message)

@bot.command()
@commands.check_any(commands.has_role('Ultimate Weebs'), commands.is_owner())
async def addcounter(ctx, letext):
    print("in addcounter")
    cur = dbconn.cursor()
    cur.execute("SELECT 1 FROM wordcount WHERE LOWER(TEXT)=?", (letext.lower(),))
    rows = cur.fetchall()
    if not rows:
        cur.execute("INSERT INTO wordcount (TEXT) VALUES (?)", (letext,))
        dbconn.commit()
        tempstring = letext + " succesfully added"
    else:
        tempstring = letext + " already exists"
    print(tempstring)
    await ctx.send(tempstring)

@bot.command()
@commands.check_any(commands.has_role('Ultimate Weebs'), commands.is_owner())
async def delcounter(ctx, letext):
    print("in delcounter")
    cur = dbconn.cursor()
    cur.execute("SELECT 1 FROM wordcount WHERE LOWER(TEXT)=?", (letext.lower(),))
    rows = cur.fetchall()
    if rows:
        cur.execute("DELETE FROM wordcount WHERE TEXT=(?)", (letext,))
        dbconn.commit()
        tempstring = letext + " succesfully removed"
    else:
        tempstring = letext + " does not exists"
    print(tempstring)
    await ctx.send(tempstring)

@bot.command()
@commands.is_owner()
async def setcounter(ctx, letext, amount):
    if not letext or not amount:
        await ctx.send("There are parameters missing. Usage: ?setcounter \"[text]\" [amount]")
    else:
        cur = dbconn.cursor()
        cur.execute("SELECT * FROM wordcount WHERE LOWER(TEXT)=?", (letext,))
        rows = cur.fetchall()
        if rows:
            amount = filterNumbers(amount)
            if hasNumbers(amount):
                cur.execute("UPDATE wordcount SET COUNT=? WHERE LOWER(TEXT)=?", (amount, letext,))
                dbconn.commit()
                await ctx.send("The count for " + letext + " has been set to " + amount)
            else:
                await ctx.send("Please enter a number as the second parameter")
        else:
            await ctx.send(letext + " cannot be found")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("You do not have the rights for using this command")

bot.run(TOKEN)
