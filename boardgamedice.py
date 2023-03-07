import random
import numpy as np
import re
import cv2
import discord

from dice import dice_sets

# Determine if the command entered is one of the available board
# game dice.
async def roll_board_game_dice(message, command, param):
    # Is the requested dice set available?
    if command in dice_sets:
        loadedDice = dice_sets[command]
        
        if (loadedDice.get('defaultDiceType')):
            default_regex = re.compile(loadedDice['defaultDiceType']['regex'])
            default_match = re.match(default_regex, param)
        else:
            default_match = False

        specific_dice_regex = re.compile(loadedDice['regex'])
        specific_match = re.match(specific_dice_regex, param)

        # Process a default set of dice, if possible
        if default_match:
            await default_dice_roll(message, loadedDice, param)
        elif specific_match:
            await specific_dice_roll(message, loadedDice, param)
        else:
            print("show usage")

async def default_dice_roll(message, loadedDice, param):
    numToRoll = int(param)

    # Does the requested dice set have a default dice?
    if loadedDice['defaultDiceType']:
        diceFaceCount = 0
        diceImages = {}
        rolledDice = []

        # We're only matching a default dice request so we only need to check the param number
        # to determine total dice rolled.
        if (int(param) <= loadedDice['maxNumberOfTotalDice'] and int(param) >= 1):
            # Assemble current dice's default individual faces
            for faceEntry in loadedDice['defaultDiceType']['faces']:

                # Current face
                currentFace = faceEntry['face']
                for x in range(0, faceEntry['numOfFaces']):
                    diceFaceCount = diceFaceCount + 1
                    diceImages[diceFaceCount] = cv2.imread(f'images/{loadedDice["imageDirectory"]}/' + currentFace, cv2.IMREAD_UNCHANGED)

            # Roll the dice and save the appropriate face to an array
            for x in range(numToRoll):
                rolledDice.append(diceImages[random.randint(1, diceFaceCount)])

            result_image = np.zeros((100, len(rolledDice) * 108, 4), np.uint8)
            result_image[:, :, 3] = 0

            x = 0
            for currentDiceFace in rolledDice:
                result_image[0 : 100, 108 * x : 108 * (x + 1), 0:3] = currentDiceFace[:, :, 0:3]
                result_image[0 : 100, 108 * x : 108 * (x + 1), 3] = currentDiceFace[:, :, 3]
                x = x + 1

            cv2.imwrite(f'images/{loadedDice["imageDirectory"]}/results.png', result_image)

            await message.channel.send(file=discord.File(f'images/{loadedDice["imageDirectory"]}/results.png'))
        else:
            await message.channel.send(f'Sorry, **{message.author.name}**, but for the {loadedDice["name"]} board game dice you must \
roll at least 1 dice up to a maximum of {str(loadedDice["maxNumberOfTotalDice"])} dice.')
    else:
            colorList = ''
            colorMessage = ''
            if loadedDice["diceTypes"].keys():
                for color in loadedDice["diceTypes"].keys():
                    colorList = colorList + " **" + color + "**"
                colorMessage = f'\n  Accepted colors are: {colorList}'
            await message.channel.send(f'Sorry, **{message.author.name}**, but for the {loadedDice["name"]} board game dice you must \
roll at least 1 dice up to a maximum of {str(loadedDice["maxNumberOfTotalDice"])} dice, and specify what colors you\'d like to roll.{colorMessage}')


async def specific_dice_roll(message, loadedDice, param):
    totalDiceRolled = 0
    diceToRoll = []
    temp = param.split(' ')
    param_sets = [' '.join(temp[i : i + 2]) for i in range(0, len(temp), 2)]
    
    for param_set in param_sets:
        split_set = param_set.split(' ')
        numberToRoll = int(split_set[0])
        colorToRoll = split_set[1]

        totalDiceRolled = totalDiceRolled + numberToRoll
        # Ensure both the current numToRoll and the cumulative total dice rolled do not exceed 15.
        if (totalDiceRolled > loadedDice['maxNumberOfTotalDice']):
            await message.channel.send(f'Sorry, but you cannot roll more than {loadedDice["maxNumberOfTotalDice"]} total combat dice in a single command.')
            return
        
        # Ensure that at least 1 die of each requested color is rolled.
        if (numberToRoll < 1):
            await message.channel.send('Sorry, but for each die color specified you must roll at least 1 die.')
            return
        
        # Ensure that the colors requested are available.
        if (colorToRoll not in loadedDice['diceTypes'].keys()):
            available_colors = '**_' + ', '.join(loadedDice['diceTypes'].keys()) + '_**'
            await message.channel.send(f'Sorry, but you\'ve included a die color that isn\'t available. Available colors are: {available_colors}.')
            return
        
        # Ensure that each dice face is only indicated once.
        for existingDice in diceToRoll:
            for dieColor in existingDice.values():
                if (colorToRoll == dieColor):
                    await message.channel.send('Sorry, but each die color can only be specified once.')
                    return
                
        diceToRoll.append({'face': colorToRoll, 'numToRoll': int(numberToRoll)})

    # Assemble current dice's faces
    diceFaceCount = 0
    diceImages = {}
    rolledDice = []

    for currentRequestedFace in diceToRoll:
        # Color of current face
        currentFaceColor = loadedDice['diceTypes'][currentRequestedFace['face']]

        # Assemble the current color's dice faces
        for coloredFace in currentFaceColor['faces']:
            for x in range(0, coloredFace['numOfFaces']):
                diceFaceCount = diceFaceCount + 1
                diceImages[diceFaceCount] = cv2.imread(f'images/{loadedDice["imageDirectory"]}/{coloredFace["face"]}', cv2.IMREAD_UNCHANGED)

        # Roll the dice and save the appropriate face to an array
        for x in range(int(currentRequestedFace['numToRoll'])):
            rolledDice.append(diceImages[random.randint(1, diceFaceCount)])

        diceFaceCount = 0
        diceImages.clear()

    result_image = np.zeros((100, len(rolledDice) * 108, 4), np.uint8)
    result_image[:, :, 3] = 0

    x = 0
    for currentDiceFace in rolledDice:
        if currentDiceFace.shape[2] == 3:
            # Add alpha channel to currentDiceFace
            currentDiceFace = np.dstack((currentDiceFace, np.full_like(currentDiceFace[:, :, 0], 255)))
        result_image[0 : 100, 108 * x : 108 * (x + 1), 0 : 3] = currentDiceFace[:, :, 0 : 3]
        result_image[0 : 100, 108 * x : 108 * (x + 1), 3] = currentDiceFace[:, :, 3]
        x = x + 1

    cv2.imwrite(f'images/{loadedDice["imageDirectory"]}/results.png', result_image)

    await message.channel.send(file=discord.File(f'images/{loadedDice["imageDirectory"]}/results.png'))