import random
import numpy as np
import cv2
import discord

async def checkOrcQuestDiceParameters(message, param):
    params = param.split(' ')
    totalDiceRolled = 0
    diceToRoll = []

    # No parameters entered. Return error message.
    if (len(params) < 1):
        await message.channel.send('Sorry, but you must specify the type of dice you\'re rolling.')
        return
    
    paramArray = np.array_split(params, len(params) / 2)


    # Iterate the sets of dice quantities and requested type/colors.
    for currentParam in paramArray:
        numToRoll = int(currentParam[0])
        currentColor = currentParam[1]
    
        totalDiceRolled = totalDiceRolled + numToRoll
        # Ensure both the current numToRoll and the cumulative total dice rolled do not exceed 10.
        if (totalDiceRolled > 10):
            await message.channel.send('Sorry, but you cannot roll more than 10 total combat dice in a single command.')
            return
        
        # Ensure that at least 1 die of each requested type & color is rolled.
        if (numToRoll < 1):
            await message.channel.send('Sorry, but for each die type & color specified you must roll at least 1 die.')
            return
        
        # Ensure that no more than 3 dice of each requested type & color is rolled.
        if (numToRoll > 3):
            await message.channel.send('Sorry, but for each die type & color specified you cannot roll more than 3 dice.')
            return
        
        # Ensure that the colors requested are available.
        if (currentColor != 'whiteattack' and currentColor != 'greyattack' and currentColor != 'blackattack' and \
                currentColor != 'whitedefend' and currentColor != 'greydefend' and currentColor != 'blackdefend' \
                and currentColor != 'greenbadass' and currentColor != 'bluebadass'):
            await message.channel.send('Sorry, but you\'ve included a die color/type combination that isn\'t available. Available color/types \
are whiteattack, greyattack, blackattack, whitedefend, greydefend, blackdefend, greenbadass or bluebadass.')
            return
        
        for existingDice in diceToRoll:
            for dieColor in existingDice.values():
                if (currentColor == dieColor):
                    await message.channel.send('Sorry, but each die color/type combination can only be specified once.')
                    return

        # Ensure that the same color was not requested more than once in a single roll command.
        #if (any(currentColor in dice for dice in diceToRoll)):
        #    await message.channel.send('Sorry, but each die color can only be specified once.')
        #    return
        #else:
        #    diceToRoll.append({'face': currentColor, 'numToRoll': int(numToRoll)})

        diceToRoll.append({'face': currentColor, 'numToRoll': int(numToRoll)})

    await rollOrcQuestCombatDice(message, diceToRoll)
    
# Function takes 3 parameters:
# 1. An array describing the dice faces of a die to be rolled and how many of each face are on that die.
# Example: [{'face': 'skull.png', 'numOfSides': 3}, {'face': 'whiteshield.png', 'numOfSides': 2}, {'face': 'blackshield.png', 'numOfSides': 1}]
# 2. The number of dice to be rolled.
# 3. The background color of the dice image, defaults to white.
async def rollOrcQuestCombatDice(message, diceToRoll):
    whiteattack = [{'face': 'white-attack-yellow.png', 'numOfFaces': 4}, {'face': 'white-attack-orange.png', 'numOfFaces': 2}]
    whitedefend = [{'face': 'white-defend-blank.png', 'numOfFaces': 2}, {'face': 'white-defend-yellow.png', 'numOfFaces': 3}, {'face': 'white-defend-orange.png', 'numOfFaces': 1}]
    greyattack = [{'face': 'grey-attack-yellow.png', 'numOfFaces': 3}, {'face': 'grey-attack-orange.png', 'numOfFaces': 2}, {'face': 'grey-attack-red.png', 'numOfFaces': 1}]
    greydefend = [{'face': 'grey-defend-blank.png', 'numOfFaces': 2}, {'face': 'grey-defend-yellow.png', 'numOfFaces': 1}, {'face': 'grey-defend-orange.png', 'numOfFaces': 3}]
    blackattack = [{'face': 'black-attack-orange.png', 'numOfFaces': 3}, {'face': 'black-attack-red.png', 'numOfFaces': 3}]
    blackdefend = [{'face': 'black-defend-blank.png', 'numOfFaces': 2}, {'face': 'black-defend-orange.png', 'numOfFaces': 2}, {'face': 'black-defend-red.png', 'numOfFaces': 2}]
    greenbadass = [{'face': 'badass-green-skull.png', 'numOfFaces': 3}, {'face': 'badass-green-lightning-bolt.png', 'numOfFaces': 2}, {'face': 'badass-green-explosion.png', 'numOfFaces': 1}]
    bluebadass = [{'face': 'badass-blue-skull.png', 'numOfFaces': 3}, {'face': 'badass-blue-lightning-bolt.png', 'numOfFaces': 2}, {'face': 'badass-blue-explosion.png', 'numOfFaces': 1}]
    diceFaceCount = 0
    diceImages = {}
    rolledDice = []

    # Assemble current dice's faces
    for currentRequestedFace in diceToRoll:

        # Color of current face
        currentFaceColor = currentRequestedFace['face']
        if (currentFaceColor == 'whiteattack'):
            currentFace = whiteattack
        elif (currentFaceColor == 'whitedefend'):
            currentFace = whitedefend
        elif (currentFaceColor == 'greyattack'):
            currentFace = greyattack
        elif (currentFaceColor == 'greydefend'):
            currentFace = greydefend
        elif (currentFaceColor == 'blackattack'):
            currentFace = blackattack
        elif (currentFaceColor == 'blackdefend'):
            currentFace = blackdefend
        elif (currentFaceColor == 'greenbadass'):
            currentFace = greenbadass
        elif (currentFaceColor == 'bluebadass'):
            currentFace = bluebadass
        
        # Assemble the current color's dice faces
        for coloredFace in currentFace:
            for x in range(0, coloredFace['numOfFaces']):
                diceFaceCount = diceFaceCount + 1
                diceImages[diceFaceCount] = cv2.imread('images/oqdice/' + coloredFace['face'], cv2.IMREAD_UNCHANGED)

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

    cv2.imwrite('images/oqdice/results.png', result_image)

    await message.channel.send(file=discord.File('images/oqdice/results.png'))