import random
import numpy as np
import cv2
import discord

async def checkDescentCombatDiceParameters(message, param):
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
        if (totalDiceRolled > 9 or (currentColor == 'red' and numToRoll > 2) or (currentColor == 'blue' and numToRoll > 1)
            or (currentColor == 'yellow' and numToRoll > 2) or (currentColor == 'brown' and numToRoll > 1)
            or (currentColor == 'gray' and numToRoll > 2) or (currentColor == 'grey' and numToRoll > 2) 
            or (currentColor == 'black' and numToRoll > 1)):
            await message.channel.send('Sorry, but you cannot roll more than 2 of red dice, more than 1 blue die, \
more than 2 of yellow dice, more than 1 of brown dice, more than 2 of gray/grey dice, more than 2 of black dice, \
and/or up to 9 total combat dice in a single command.')
            return
        
        # Ensure that at least 1 die of each requested color is rolled.
        if (numToRoll < 1):
            await message.channel.send('Sorry, but for each die color specified you must roll at least 1 die.')
            return
        
        # Ensure that the colors requested are available.
        if (currentColor != 'red' and currentColor != 'blue' and currentColor != 'yellow' 
            and currentColor != 'brown' and currentColor != 'gray' and currentColor != 'grey' 
            and currentColor != 'black'):
            await message.channel.send('Sorry, but you\'ve included a die color that isn\'t available. Available colors \
are red, blue, yellow, brown, gray/grey, and black.')
            return
        
        for existingDice in diceToRoll:
            for dieColor in existingDice.values():
                if (currentColor == dieColor):
                    await message.channel.send('Sorry, but each die color can only be specified once.')
                    return

        diceToRoll.append({'face': currentColor, 'numToRoll': int(numToRoll)})

    await rollDescentCombatDice(message, diceToRoll)
    
# Function takes 3 parameters:
# 1. An array describing the dice faces of a die to be rolled and how many of each face are on that die.
# Example: [{'face': 'red-1heart.png', 'numOfFaces': 1}, {'face': 'red-2hearts.png', 'numOfFaces': 3}, {'face': 'red-3hearts.png', 'numOfFaces': 1}, {'face': 'red-3hearts-1surge.png', 'numOfFaces': 1}]
# 2. The number of dice to be rolled.
async def rollDescentCombatDice(message, diceToRoll):
    red = [{'face': 'red-1heart.png', 'numOfFaces': 1}, {'face': 'red-2hearts.png', 'numOfFaces': 3}, {'face': 'red-3hearts.png', 'numOfFaces': 1}, {'face': 'red-3hearts-1surge.png', 'numOfFaces': 1}]
    blue = [{'face': 'blue-miss.png', 'numOfFaces': 1}, {'face': 'blue-number2-2hearts-1surge.png', 'numOfFaces': 1}, {'face': 'blue-number3-2hearts.png', 'numOfFaces': 1}, {'face': 'blue-number4-2hearts.png', 'numOfFaces': 1}, {'face': 'blue-number5-1heart.png', 'numOfFaces': 1}, {'face': 'blue-number6-1heart-1surge.png', 'numOfFaces': 1}]
    yellow = [{'face': 'yellow-2hearts.png', 'numOfFaces': 1}, {'face': 'yellow-1heart-1surge.png', 'numOfFaces': 1}, {'face': 'yellow-number1-1heart.png', 'numOfFaces': 1}, {'face': 'yellow-number1-1surge.png', 'numOfFaces': 1}, {'face': 'yellow-number2-1heart.png', 'numOfFaces': 1}, {'face': 'yellow-2hearts-1surge.png', 'numOfFaces': 1}]
    brown = [{'face': 'brown-blank.png', 'numOfFaces': 3}, {'face': 'brown-1shield.png', 'numOfFaces': 2}, {'face': 'brown-2shields.png', 'numOfFaces': 1}]
    gray = [{'face': 'gray-blank.png', 'numOfFaces': 1}, {'face': 'gray-1shield.png', 'numOfFaces': 3}, {'face': 'gray-2shields.png', 'numOfFaces': 1}, {'face': 'gray-3shields.png', 'numOfFaces': 1}]
    black = [{'face': 'black-blank.png', 'numOfFaces': 1}, {'face': 'black-2shields.png', 'numOfFaces': 3}, {'face': 'black-3shields.png', 'numOfFaces': 1}, {'face': 'black-4shields.png', 'numOfFaces': 1}]
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
        elif (currentFaceColor == 'brown'):
            currentFace = brown
        elif (currentFaceColor == 'gray' or currentFaceColor == 'grey'):
            currentFace = gray
        elif (currentFaceColor == 'black'):
            currentFace = black
        
        # Assemble the current color's dice faces
        for coloredFace in currentFace:
            for x in range(0, coloredFace['numOfFaces']):
                diceFaceCount = diceFaceCount + 1
                diceImages[diceFaceCount] = cv2.imread('images/descent/' + coloredFace['face'], cv2.IMREAD_UNCHANGED)

        # Roll the dice and save the appropriate face to an array
        for x in range(int(currentRequestedFace['numToRoll'])):
            rolledDice.append(diceImages[random.randint(1, 6)])
                
        diceFaceCount = 0
        diceImages.clear()

    result_image = np.zeros((100, len(rolledDice) * 108, 4), np.uint8)
    result_image[:, :, 3] = 0

    x = 0
    for currentDiceFace in rolledDice:
        result_image[0 : 100, 108 * x : 108 * (x + 1), 0:3] = currentDiceFace[:, :, 0:3]
        result_image[0 : 100, 108 * x : 108 * (x + 1), 3] = currentDiceFace[:, :, 3]
        x = x + 1

    cv2.imwrite('images/descent/results.png', result_image)

    await message.channel.send(file=discord.File('images/descent/results.png'))