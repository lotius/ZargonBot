import random
import os
import cv2
import numpy as np
import discord

async def process_command(message, command, param):
    if (command == 'help'):
        await help(message)
    elif (command == 'roll'):
        await roll(message, param)
    elif (command == 'hqroll'):
        await heroquest_roll(message, param)
    elif (command == 'terry'):
        await terry(message)
    elif (command == 'disappointed'):
        await disappointed(message)

def can_convert_to_int(string):
    try:
        int(string)

        return True
    except ValueError:
        return False

async def help(message):
    if(int(message.guild.id) == int(os.getenv('MY_DISCORD_GUILD_ID'))):
        await message.channel.send(f'Command List:\n \
        !roll - Roll a specified set of dice faces.\n \
        !hqroll - Roll the HeroQuest combat dice.\n \
        !terry - Post a random Terry A. Davis picture.\n \
        !disappointed - Kevin Sorbo is very disappointed.')
    else:
        await message.channel.send(f'Command List:\n \
        !roll - Roll a specified set of dice faces.\n \
        !hqroll - Roll the HeroQuest combat dice.\n')

async def roll(message, param):
    dice = param.split('d', 1)
    diceTotalDetail = []

    if (len(dice) != 2 or not can_convert_to_int(dice[0]) or not can_convert_to_int(dice[1]) or int(dice[0]) > 10 or int(dice[1]) > 100):
        await message.channel.send('Proper roll format is #d#! (Example: !roll 2d6). Maximum of 10 die and 100 sides.')
        return

    for x in range(int(dice[0])):
        diceTotalDetail.append(random.randint(1, int(dice[1])))

    await message.channel.send(f'**{message.author.name}** rolled **{sum(diceTotalDetail)}** _{diceTotalDetail}_.')

async def heroquest_roll(message, param):
    image = cv2.imread('images/hqdice/dicefaces.png', cv2.IMREAD_COLOR)
    skull = image[0 : 100, 0 : 110] # y1:y2, x1:x2
    whiteshield = image[0 : 100, 110 : 220]
    blackshield = image[0 : 100, 220 : 330]
    diceRolls = []

    if (can_convert_to_int(param) and int(param) > 0 and int(param) <= 15):
        for x in range(int(param)):
            diceRolls.append(random.randint(1, 6))
    else:
        await message.channel.send('HeroQuest combat roll command usage: !hqroll # (Example: !hqroll 3). Max roll of 15.')
        return
    
    result_image = np.zeros((100, len(diceRolls) * 110, 3), np.uint8)
    for x in range(len(diceRolls)):
        if (diceRolls[x] == 1 or diceRolls[x] == 2 or diceRolls[x] == 3):
            result_image[0 : 100, 110 * x : 110 * (x + 1)] = skull
        elif (diceRolls[x] == 4 or diceRolls[x] == 5):
            result_image[0 : 100, 110 * x : 110 * (x + 1)] = whiteshield
        elif (diceRolls[x] == 6):
            result_image[0 : 100, 110 * x : 110 * (x + 1)] = blackshield
    
    cv2.imwrite('images/hqdice/results.png', result_image)

    await message.channel.send(file=discord.File('images/hqdice/results.png'))

async def terry(message):
    if(int(message.guild.id) == int(os.getenv('MY_DISCORD_GUILD_ID'))):
        path = 'images/terry'
        files = os.listdir(path)

        file_to_send = files[random.randint(0, len(files) - 1)]
    
        await message.channel.send(file=discord.File(f'images/terry/{file_to_send}'))

async def disappointed(message):
    if(int(message.guild.id) == int(os.getenv('MY_DISCORD_GUILD_ID'))):
        await message.channel.send(file=discord.File(f'images/disappointed.gif'))