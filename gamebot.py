import os
import commands
import discord
import pytz

import requests
from random import randint
from time import sleep
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from discord.ext import tasks
from datetime import datetime, timedelta
from dotenv import load_dotenv

# URL to poll, and the search title to poll for
instruction_url = 'https://instructions.hasbro.com/en-us/all-instructions?search=heroquest'
title = 'Against the Ogre Horde'

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_NAME = os.getenv('MY_DISCORD_GUILD')
RIBBY_CHANNEL_ID = os.getenv('RIBBY_CHANNEL_ID')
RIBBY_CHANNEL_NAME = os.getenv('RIBBY_CHANNEL_NAME')
GENERAL_CHANNEL_NAME = os.getenv('GENERAL_CHANNEL_NAME')

intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)

@tasks.loop(minutes = 1)
async def weekly_message():
    # Calculate the next Tuesday at 1 PM
    target_time = datetime.now(pytz.timezone("America/Chicago")).replace(hour=13, minute=0, second=0, microsecond=0)
    
    days_ahead = 1 - target_time.weekday()  # 1 corresponds to Tuesday
    if days_ahead <= 0:  # If today is Tuesday and we are past 1 PM, set for next week
        days_ahead += 7

    target_time += timedelta(days=days_ahead)
    await discord.utils.sleep_until(target_time)

    channel = discord.utils.get(client.get_all_channels(), name = RIBBY_CHANNEL_NAME)
    
    if channel:
        await channel.send(file=discord.File('images/bisontuesday.gif'))
    else:
        print(f"Channel with name '{RIBBY_CHANNEL_NAME}' not found.")

@tasks.loop(minutes=1)
async def new_instructions_available():
    response = requests.get(instruction_url)

    if response.text.find(title) != -1:  # Check if the title is found in the response
        filename = f"{title}.txt"  # Create a filename based on the title
        if not os.path.isfile('found_instructions/' + filename):  # Check if the file doesn't exist
            print('Found ' + title + '!')
            channel = discord.utils.get(client.get_all_channels(), name=GENERAL_CHANNEL_NAME)
            if channel:
                await channel.send(f"Hey everyone! This is just to inform you that the new quest booklet for {title} is now available on the Hasbro Instructions webpage! https://instructions.hasbro.com")
                # Write the filename to indicate the quest booklet has been processed
                with open('found_instructions/' + filename, 'w') as file:
                    file.write(f"{title} processed")
            else:
                print(f"Channel with name '{GENERAL_CHANNEL_NAME}' not found.")


#@client.event
#async def on_member_join(member):
    # get general channel object here
#    if (int(member.guild.id) == int(os.getenv('MY_DISCORD_GUILD_ID'))):
#        welcome_message = 'Welcome, ' + member.name + '! If you\'d like access to the GM (Zargon/Morcar) channel please let us know.'
#        #await channel.send(welcome_message)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    guild = discord.utils.get(client.guilds, name=GUILD_NAME)

    print(
        f'{client.user} is connected to the following guild(s):\n' \
        f'{guild.name} (id: {guild.id})'
    )

    # Start the scheduled tasks
    weekly_message.start()
    new_instructions_available.start()
    
@client.event
async def on_message(message):
    command = ""
    params = ""
    
    if ((message.channel.id == int(os.getenv('RIBBY_CHANNEL_ID')) or not message.guild.id == int(os.getenv('MY_DISCORD_GUILD_ID'))) and message.author.bot == False and not message.attachments and not message.is_system()):  
        if (message.content[0] == '!' and len(message.content) > 1):

            space_position = message.content.find(' ')
            
            if (space_position != -1):
                command = message.content[1:space_position]
                params = message.content[space_position + 1:]
            else:
                command = message.content[1:]

            await commands.process_command(message, command, params)
    else:
        return

client.run(TOKEN)