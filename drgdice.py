import random
import numpy as np
import cv2
import discord

async def checkDRGCombatDiceParameters(message, param):
    params = param.split(' ')
    totalDiceRolled = 0
    diceToRoll = []
    
    paramArray = np.array_split(params, len(params) / 2)

    # Iterate the sets of dice quantities and requested colors.
    for currentParam in paramArray:
        numToRoll = int(currentParam[0])
        currentColor = currentParam[1]
    
        totalDiceRolled = totalDiceRolled + numToRoll
        # Ensure both the current numToRoll and the cumulative total dice rolled do not exceed 9, and
        # red is only rolled up to 2 times, blue only rolled up to 1 time, yellow only rolled up to 
        # 2 times, brown only rolled up to 1 time, gray only rolled up to 2 times, and black only
        # rolled up to 1 time.
        if (totalDiceRolled > 3 or (currentColor == 'red' and numToRoll > 2) or (currentColor == 'blue' and numToRoll > 2)
            or (currentColor == 'yellow' and numToRoll > 3) or (currentColor == 'green' and numToRoll > 3)
            or (currentColor == 'white' and numToRoll > 2) or (currentColor == 'black' and numToRoll > 2) 
            or (currentColor == 'gray' and numToRoll > 1)):
            await message.channel.send('Sorry, but you cannot roll more than 2 of red dice, more than 2 blue die, \
more than 3 of yellow dice, more than 3 of green dice, more than 1 of gray/grey dice, more than 2 of black dice, \
more than 2 white dice, and/or up to 3 total dice in a single command.')
            return
        
        # Ensure that at least 1 die of each requested color is rolled.
        if (numToRoll < 1):
            await message.channel.send('Sorry, but for each die color specified you must roll at least 1 die.')
            return
        
        # Ensure that the colors requested are available.
        if (currentColor != 'red' and currentColor != 'blue' and currentColor != 'yellow' 
            and currentColor != 'green' and currentColor != 'gray' and currentColor != 'grey' 
            and currentColor != 'black' and currentColor != 'white'):
            await message.channel.send('Sorry, but you\'ve included a die color that isn\'t available. Available colors \
are red, blue, yellow, green, gray/grey, white, and black.')
            return
        
        for existingDice in diceToRoll:
            for dieColor in existingDice.values():
                if (currentColor == dieColor):
                    await message.channel.send('Sorry, but each die color can only be specified once.')
                    return

        diceToRoll.append({'face': currentColor, 'numToRoll': int(numToRoll)})

    await rollDRGCombatDice(message, diceToRoll)
    
# Function takes 2 parameters:
# 1. An array describing the dice faces of a die to be rolled and how many of each face are on that die.
# Example: [{'face': 'green-bullet.png', 'numOfFaces': 4}, {'face': 'green-blank.png', 'numOfFaces': 2}]
# 2. The number of dice to be rolled.
async def rollDRGCombatDice(message, diceToRoll):
    red = [{'face': 'red-1explosion.png', 'numOfFaces': 3}, {'face': 'red-2explosions.png', 'numOfFaces': 2}, {'face': 'red-movecreature.png', 'numOfFaces': 1}]
    blue = [{'face': 'blue-1piercing.png', 'numOfFaces': 3}, {'face': 'blue-2piercing.png', 'numOfFaces': 2}, {'face': 'blue-blank.png', 'numOfFaces': 1}]
    yellow = [{'face': 'yellow-1flame.png', 'numOfFaces': 3}, {'face': 'yellow-2flames.png', 'numOfFaces': 1}, {'face': 'yellow-blank.png', 'numOfFaces': 2}]
    green = [{'face': 'green-bullet.png', 'numOfFaces': 4}, {'face': 'green-blank.png', 'numOfFaces': 2}]
    gray = [{'face': 'gray-gold.png', 'numOfFaces': 2}, {'face': 'gray-nitra.png', 'numOfFaces': 2}, {'face': 'gray-blank.png', 'numOfFaces': 2}]
    white = [{'face': 'white-1pickaxe.png', 'numOfFaces': 3}, {'face': 'white-2pickaxes.png', 'numOfFaces': 2}, {'face': 'white-blank.png', 'numOfFaces': 1}]
    black = [{'face': 'black-damage.png', 'numOfFaces': 3}, {'face': 'black-specialeffect.png', 'numOfFaces': 2}, {'face': 'black-blank.png', 'numOfFaces': 1}]
    diceFaceCount = 0
    diceImages = {}
    rolledDice = []

    # Assemble current dice's faces
    for currentRequestedFace in diceToRoll:

        # Color of current face
        currentFaceColor = currentRequestedFace['face']
        if (currentFaceColor == 'red'):
            currentFace = red
        elif (currentFaceColor == 'blue'):
            currentFace = blue
        elif (currentFaceColor == 'yellow'):
            currentFace = yellow
        elif (currentFaceColor == 'green'):
            currentFace = green
        elif (currentFaceColor == 'gray' or currentFaceColor == 'grey'):
            currentFace = gray
        elif (currentFaceColor == 'white'):
            currentFace = white
        elif (currentFaceColor == 'black'):
            currentFace = black
        
        # Assemble the current color's dice faces
        for coloredFace in currentFace:
            for x in range(0, coloredFace['numOfFaces']):
                diceFaceCount = diceFaceCount + 1
                diceImages[diceFaceCount] = cv2.imread('images/drg/' + coloredFace['face'], cv2.IMREAD_COLOR)

        # Roll the dice and save the appropriate face to an array
        for x in range(int(currentRequestedFace['numToRoll'])):
            rolledDice.append(diceImages[random.randint(1, 6)])
                
        diceFaceCount = 0
        diceImages.clear()

    result_image = np.zeros((100, len(rolledDice) * 108, 3), np.uint8)
    x = 0
    for currentDiceFace in rolledDice:
        result_image[0 : 100, 108 * x : 108 * (x + 1)] = currentDiceFace
        x = x + 1

    cv2.imwrite('images/drg/results.png', result_image)

    await message.channel.send(file=discord.File('images/drg/results.png'))