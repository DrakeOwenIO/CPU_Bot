import abc
from datetime import datetime, date, timedelta
from time import timezone
import discord
import asyncio
from discord import message
from discord import colour
from discord import channel
from discord.channel import TextChannel
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord.abc import Messageable
from discord.message import Message
import random

# Command prefix
client = commands.Bot(command_prefix = '+', case_insensitive=True)
client.launch_time = datetime.utcnow()

# Set the play status
@client.event
async def on_ready():
    # Setting `Playing ` status
    await client.change_presence(activity=discord.Game(name="On Satellite Internet"))
    print('Bot is ready.')

# Changelog command
@client.command()
async def changelog(ctx):

    await ctx.channel.purge(limit = 1)

    embed = discord.Embed(
        title = 'Change Log',
        description = 'Heres what changed! Version Number: v1.3.1 (The Insult Update!)\n\n Gather one! Gather all! For the Insult update! Have you ever wanted to insult your friends but dont exactly know what to say? Well have no fear because CPU_Bot has your back! Simply type +insult along with the name of your friend and CPU_Bot will do the work for you. You dont even have to take the blame for it because CPU_Bot will delete your message and take all the blame for you. If you want to see a list of all the insults type "+insult list". I also added a +gay command but you can figure out how that works. I also fixed the +remind bug where you had to enclose your words in quotes. You no longer have to do that.',
        colour = discord.Colour.blue()
    )
    embed.add_field(name="New Commands", value="----------------------------------", inline=False)
    embed.add_field(name="Insult [@person to insult]", value="Randomly insults person of your choice.", inline=False)
    embed.add_field(name="Gay [direction]", value="You can figure out what this does. Hint: above/below", inline=False)
    embed.add_field(name='Say [Whatever you want the bot to say]', value="Repeats whatever you want the bot to say.", inline=False)
    embed.add_field(name="||Removed Herobrine||", value="||[REDACTED]||", inline=False)

    await ctx.send(embed=embed)

# Uptime command
@client.command()
async def uptime(ctx):
    delta_uptime = datetime.utcnow() - client.launch_time #Calculates Bot Uptime
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    await ctx.send("CPU_Bot has been running for " + f"{days}d {hours}h {minutes}m")

# Delete messages
@client.command(pass_context = True)
async def delete(ctx, number):
    number = int(number) #Converting the amount of messages to delete to an integer
    await ctx.send("Deleting...")
    await ctx.channel.purge(limit = number + 2)

# Reminder
@client.command(pass_context = True)
async def remind(ctx, hours, minutes, *remindMessage):

    totalHours = int(hours) * 3600
    totalMinutes = int(minutes) * 60
    timeObject = (int(totalHours)) + int(totalMinutes)

    remindMessage = ' '.join(remindMessage)

    mention = ctx.author.mention

    await ctx.send("I will remind you in " + hours + " hours and " + minutes + " minutes: " + remindMessage)

    await asyncio.sleep (int(timeObject))

    response = f"{mention} Here's your reminder: {remindMessage}"

    await ctx.send(response)

# Current time in various time zones
@client.command()
async def current(ctx, timeZoneAbv):

    currentTime = datetime.now()

    timeZoneAbv = timeZoneAbv.lower()

    if (timeZoneAbv == "est"):
        currentTime
        timeZoneAbv = "Eastern"

    elif (timeZoneAbv == "utc"):
        currentTime = datetime.utcnow()
        timeZoneAbv = "Universal"

    elif (timeZoneAbv == "cst"):
        currentTime = currentTime - timedelta(hours = 1)
        timeZoneAbv = "Central"

    elif (timeZoneAbv == "mst"):
        currentTime = currentTime - timedelta(hours = 2)
        timeZoneAbv = "Mountain"

    elif (timeZoneAbv == "pst"):
        currentTime = currentTime - timedelta(hours = 3)
        timeZoneAbv = "Pacific"

    else:
        response = "The timezone " + timeZoneAbv + " does not exist or has not been added yet."
        await ctx.send(response)
        return
    
    hours = currentTime.hour
    minutes = currentTime.minute

    response = "The current time in the " + timeZoneAbv + " timezone is " + f"{hours}:{minutes}"

    await ctx.send(response)

# Insults
@client.command(pass_context = True)
async def insult(ctx, userToInsult):

    insultList = ["Fuck you.", "Fucking asshole.", "You're so fat I bet you fall off both sides of the bed.", "I'm not a cactus expert but I know a prick when I see one.", "Remember to look both ways when you go fuck yourself.", "is retarded.", "drinks plain milk and colors outside the lines.", "has a single digit iq.", "Your family tree is a wreath.", "If you were anymore inbred, you would be a sandwich.", "I bet your birth certificate is an apology from the condom factory.", "Those penis enlargement pills must be working, you're twice the dick you were yesterday.", "probably kicks puppies."]

    insultString = random.choice(insultList)

    response = userToInsult + " " + insultString

    if (userToInsult == "list"):

        await ctx.send("```" + "\n\n".join(insultList) + "```")

    else:

        await ctx.channel.purge(limit = 1)
        await ctx.send(response)

@client.command(pass_context = True)
async def gay(ctx, direction):

    direction = direction.lower()

    if (direction == "above"):
        await ctx.channel.purge(limit = 1)
        await ctx.send(file=discord.File('imgs/above.jpg'))

    elif (direction == "below"):
        await ctx.send(file=discord.File('imgs/below.jpg'))

@client.command(pass_context = True)
async def say(ctx, *whatYouWantBotToSay):

    await ctx.channel.purge(limit = 1)

    response = ' '.join(whatYouWantBotToSay)

    await ctx.send(response)

#CPU_Bot Key
#client.run('')

#Test Bot Key
client.run('')