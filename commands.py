import random
import os
import re
import discord

from hqdice import checkHeroQuestCombatDiceParameters
from scdice import checkSpaceCrusadeCombatDiceParameters
from doomdice import checkDoomCombatDiceParameters
from descentdice import checkDescentCombatDiceParameters
from drgdice import checkDRGCombatDiceParameters

async def process_command(message, command, param):
    if (command == 'help'):
        await help(message, param)
    elif (command == 'roll' or command == 'dice'):
        await roll(message, param)
    elif (command == 'hqroll' or command == 'hqdice'):
        await heroquest_roll(message, param)
    elif (command == 'scroll' or command == 'sqroll' or command == 'scdice' or command == 'sqdice'):
        await spacecrusade_roll(message, param)
    elif (command == 'doomroll' or command == 'doomdice'):
        await doom_roll(message, param)
    elif (command == 'descentroll' or command == 'descentdice'):
        await descent_roll(message, param)
    elif (command == 'drgroll' or command == 'drgdice'):
        await drg_roll(message, param)
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

async def help(message, param):
    if (len(param) == 0):
        await message.channel.send(f'Command List:\n \
!roll - Roll a specified set of dice faces. For example, if you\'d like to roll a 2d6 type: !roll 2d6\n \
!hqroll - Roll the HeroQuest combat dice. For example, if you\'d like to roll 3 combat dice type: !hqroll 3\n \
!scroll or !sqroll - Roll the Space Crusade combat dice. For example, if you\'d like to roll 2 white \
combat dice type: !scroll 2 white\n \
!doomdice - Roll the DOOM 2016 board game combat dice. For example, if you\'d like to roll 2 red \
combat dice type: !doomdice 2 red\n \
!descentdice - Roll the Descent 2nd Edition board game combat dice. For example, if you\'d like to roll 2 red \
combat dice type: !descentdice 2 red\n \
!terry - Post a random Terry A. Davis picture.\n \
!disappointed - Kevin Sorbo is very disappointed.\n \
Use !help _command_ to get more specific information about an available command.')
    elif (param == 'roll'):
        await message.channel.send(f'**Roll standard dice**:\n \
To roll standard dice use the _**!roll**_ command followed by the number of dice you wish to roll (up to 10), followed by \
how many sides each die will have (up to 100). If you leave off the number of dice you wish to roll and only input the \
number of sides for the die to have the bot will roll 1 die (ie !roll d100)\n \
_Examples: !roll 2d6, !roll d20, !roll 3d4, !roll d100_')
    elif (param == 'hqroll'):
        await message.channel.send(f'**Roll HeroQuest combat dice**:\n \
To roll HeroQuest dice use the _**!hqroll**_ command followed by the number of dice you wish \
to roll (up to 15). Optionally, you can include one of the 5 German variant dice colors \
in order to roll that set instead of standard dice, and even multiple colors at once.\n\n \
Available variant dice colors are blue, orange, green, purple, yellow, and black.\n \
**Examples:** _**!hqroll 2**, **!hqroll 5**, **!hqroll 6 orange**, **!hqroll 4 green**_\n \
You can also specify multiple dice colors in a single command\n \
**Examples:** _**!hqroll 2 white 2 orange**, **!hqroll 1 white 3 green 2 blue**_')
    elif (param == 'scroll' or param == 'sqroll' or param == 'scdice' or param == 'sqdice'):
        await message.channel.send(f'**Roll Space Crusade combat dice**:\n \
To roll Space Crusade dice use the _**!scroll**_ or _**!sqroll**_ command followed by the \
number of dice you wish to roll, followed by the color you wish to roll. In Space Crusade \
you can roll up to 4 white and up to 4 red dice.\n \
**Examples:** _**!scroll 2 white**, **!scroll 1 red 3 white**, **!sqroll 1 white 2 red**_')
    elif (param == 'doomroll' or param == 'doomdice'):
        await message.channel.send(f'**Roll DOOM (2016) combat dice**:\n \
To roll DOOM dice use the _**!doomroll**_ or _**!doomdice**_ command followed by the \
number of dice you wish to roll, followed by the color you wish to roll. In the DOOM 2016 \
board game you can roll up to 4 red and up to 2 black dice.\n \
**Examples:** _**!doomdice 2 red**, **!doomdice 2 red 2 black**, **!doomdice 1 red 3 black**_')
    elif (param == 'descentroll' or param == 'descentdice'):
        await message.channel.send(f'**Roll Descent 2nd Edition combat dice**:\n \
To roll Descent dice use the _**!descentroll**_ or _**!descentdice**_ command followed by the \
number of dice you wish to roll, followed by the color you wish to roll. In the Descent 2e \
board game you can roll up to 2 red, 1 blue, 2 yellow, 1 brown, 2 gray/grey, and 1 black dice.\n \
**Examples:** _**!descentdice 2 red**, **!descentdice 2 red 1 blue**, **!descentdice 1 brown 1 gray**_')
    elif (param == 'drgroll' or param == 'drgdice'):
        await message.channel.send(f'**Deep Rock Galactic board game dice**:\n \
To roll Deep Rock Galactic dice use the _**!drgroll**_ or _**!drgdice**_ command followed by the \
number of dice you wish to roll, followed by the color you wish to roll. In the DRG \
board game you can roll up to 2 red, 2 blue, 3 yellow, 3 green, 1 gray/grey, 2 white, and 2 black dice.\n \
**Examples:** _**!drgdice 2 yellow**, **!drgdice 2 red**, **!drgdice 3 green**_')
    elif (param == 'terry'):
        await message.channel.send(f'**Terry A. Davis**:\n \
This command displays a random image of our Lord and Savior, Terry A. Davis.')
    elif (param == 'disappointed'):
        await message.channel.send(f'**Kevin Sorbo is disappointed**:\n \
Sorbo is very disappointed.')

async def roll(message, param):
    diceTotalDetail = []
    regex = re.compile(r'^(([1-9]|10)?[dD]([1-9][0-9]?$|100))$')

    # Guarantee either d# or #d# was entered using the regex pattern.
    if (re.match(regex, param)):
        dice = param.split('d', 1)

        # User entered a number after the d only, roll 1 die.
        if (dice[0] == ''):
            diceTotalDetail.append(random.randint(1, int(dice[1])))
        # User entered 1 to 10 dice, and 1 to 100 sides.
        else:
            for x in range(int(dice[0])):
                diceTotalDetail.append(random.randint(1, int(dice[1])))
    else:
        await message.channel.send('Proper roll format is #d#! (Example: !roll 2d6). Maximum of 10 die and 100 sides.')
        return

    await message.channel.send(f'**{message.author.name}** rolled **{sum(diceTotalDetail)}** _{diceTotalDetail}_.')

async def heroquest_roll(message, param):
    # Determine if regex was matched. A digit can be matched by itself, or a combination of a digit followed by a
    # word can be matched. If a digit and word combination is matched it is allowed to be repeated.
    regex = re.compile(r'^(\d{1,2}|(\d{1,2}\s[a-zA-Z]+\b\s?)+)$')

    match = re.match(regex, param)
    if match:
        await checkHeroQuestCombatDiceParameters(message, param)
    else:
        await message.channel.send(f'**{message.author.name}** your input pattern is invalid! Please use _!help hqroll_ \
to review the proper usage of the _hqroll_ command.')
        return

async def spacecrusade_roll(message, param):
    # Determine if regex was matched. A combination of a digit followed by a
    # word can be matched up to 2 times as there are only red and white dice in Space Crusade.
    regex = re.compile(r'^(\d{1}\s[a-zA-Z]+\b\s?){1,2}$')

    match = re.match(regex, param)
    if match:
        await checkSpaceCrusadeCombatDiceParameters(message, param)
    else:
        await message.channel.send(f'**{message.author.name}** your input pattern is invalid! Please use _!help scroll_ \
to review the proper usage of the _scroll_ command.')
        return
    
async def doom_roll(message, param):
    # Determine if regex was matched. A combination of a digit followed by a
    # word can be matched up to 2 times as there are only red and black dice in DOOM.
    regex = re.compile(r'^(\d{1}\s[a-zA-Z]+\b\s?){1,2}$')

    match = re.match(regex, param)
    if match:
        await checkDoomCombatDiceParameters(message, param)
    else:
        await message.channel.send(f'**{message.author.name}** your input pattern is invalid! Please use _!help doomdice_ \
to review the proper usage of the _doomdice_ command.')
        return
    
async def descent_roll(message, param):
    # Determine if regex was matched. A combination of a digit followed by a
    # word can be matched many times to cover all possible combat rolls.
    regex = re.compile(r'^(\d{1}\s[a-zA-Z]+\b\s?)+$')

    match = re.match(regex, param)
    if match:
        await checkDescentCombatDiceParameters(message, param)
    else:
        await message.channel.send(f'**{message.author.name}** your input pattern is invalid! Please use _!help descentdice_ \
to review the proper usage of the _descentdice_ command.')
        return
    
async def drg_roll(message, param):
    # Determine if regex was matched. A combination of a digit followed by a
    # word can be matched many times to cover all possible combat rolls.
    regex = re.compile(r'^(\d{1}\s[a-zA-Z]+\b\s?)+$')

    match = re.match(regex, param)
    if match:
        await checkDRGCombatDiceParameters(message, param)
    else:
        await message.channel.send(f'**{message.author.name}** your input pattern is invalid! Please use _!help drgdice_ \
to review the proper usage of the _drgdice_ command.')
        return
    
async def terry(message):
    path = 'images/terry'
    files = os.listdir(path)

    file_to_send = files[random.randint(0, len(files) - 1)]

    await message.channel.send(file=discord.File(f'images/terry/{file_to_send}'))

async def disappointed(message):
    await message.channel.send(file=discord.File(f'images/disappointed.gif'))