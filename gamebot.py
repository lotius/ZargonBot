import os
import commands
import discord
import pytz

from discord.ext import tasks
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_NAME = os.getenv('MY_DISCORD_GUILD')
RIBBY_CHANNEL_ID = os.getenv('RIBBY_CHANNEL_ID')

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

    channel = client.get_channel(RIBBY_CHANNEL_ID)
    
    if channel:
        await channel.send(file=discord.File('images/bisontuesday.gif'))
    else:
        print(f"Channel with ID {RIBBY_CHANNEL_ID} not found.")

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
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name} (id: {guild.id})'
    )

    # Start the scheduling task
    weekly_message.start()
    
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