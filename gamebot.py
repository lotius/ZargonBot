# bot.py
import os
import commands

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    # guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    guild = discord.utils.get(client.guilds, name=GUILD)

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = ""
    for member in guild.members:
        members += "\n - " + member.name + " (" + str(member.id) + ")"

    #members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@client.event
async def on_message(message):
    command = ""
    params = ""

    if (message.channel.name == 'ribbys-hall-of-wonders' and message.author.bot == False and not message.attachments and not message.is_system()): 
        if (message.content[0] == '!' and len(message.content) > 1):

            space_position = message.content.find(' ')
            
            if (space_position != -1):
                command = message.content[1:space_position]
                params = message.content[space_position + 1:]
            else:
                command = message.content[1:]

            #print(f'Command entered: {command}')
            #print(f'Parameters entered: {params}')

            await commands.process_command(message, command, params)
    else:
        return

client.run(TOKEN)

 