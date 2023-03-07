dice_sets = {
    'hqdice': {
        'name': 'HeroQuest',
        'maxNumberOfTotalDice': 15,
        'imageDirectory': 'hqdice',
        'regex': r'^(\d{1,2}\s[a-zA-Z]+\b\s?)+$',
        'usage': 'Usage:\n  **_!hqdice #_** to roll white standard dice (Ex. **_!hqdice 3_**)\n  **_!hqdice # color_** to roll variant dice, multiple numbers and colors are accepted. (Ex. **_!hqdice 3 white 2 orange_**)',
        'help': '**Roll HeroQuest combat dice**:\n \
To roll HeroQuest dice use the _**!hqroll**_ command followed by the number of dice you wish \
to roll (up to 15). Optionally, you can include one of the 5 German variant dice colors \
in order to roll that set instead of standard dice, and even multiple colors at once.\n\n \
Available variant dice colors are blue, orange, green, purple, yellow, and black.\n \
**Examples:** _**!hqroll 2**, **!hqroll 5**, **!hqroll 6 orange**, **!hqroll 4 green**_\n \
You can also specify multiple dice colors in a single command\n \
**Examples:** _**!hqroll 2 white 2 orange**, **!hqroll 1 white 3 green 2 blue**_',
        'defaultDiceType': {
            'regex': r'^\d{1,2}$',
            'maxNumberOfDiceType': None,
            'faces': [{'face': 'skull.png', 'numOfFaces': 3}, {'face': 'whiteshield.png', 'numOfFaces': 2}, {'face': 'blackshield.png', 'numOfFaces': 1}]
        },
        'diceTypes': {
        	'white': {
            	'maxNumberOfDiceType': None, 
                'faces': [{'face': 'skull.png', 'numOfFaces': 3}, {'face': 'whiteshield.png', 'numOfFaces': 2}, {'face': 'blackshield.png', 'numOfFaces': 1}]
            },
            'blue': {
                'maxNumberOfDiceType': None,
                'faces': [{'face': 'skull-blue.png', 'numOfFaces': 3}, {'face': 'whiteshield-blue.png', 'numOfFaces': 1}, {'face': 'blackshield-blue.png', 'numOfFaces': 2}]
            },
            'orange': {
            	'maxNumberOfDiceType': None,
                'faces': [{'face': 'skull-orange.png', 'numOfFaces': 1}, {'face': 'doubleskull-orange.png', 'numOfFaces': 2}, {'face': 'doublewhiteshield-orange.png', 'numOfFaces': 1}, {'face': 'blackshield-orange.png', 'numOfFaces': 1}, {'face': 'doubleblackshield-orange.png', 'numOfFaces': 1}]
            },
            'green': {
            	'maxNumberOfDiceType': None,
                'faces': [{'face': 'skull-green.png', 'numOfFaces': 2}, {'face': 'whiteshield-green.png', 'numOfFaces': 3}, {'face': 'blackshield-green.png', 'numOfFaces': 1}]
            },
            'purple': {
            	'maxNumberOfDiceType': None,
                'faces': [{'face': 'skull-purple.png', 'numOfFaces': 2}, {'face': 'doubleskull-purple.png', 'numOfFaces': 1}, {'face': 'whiteshield-purple.png', 'numOfFaces': 1}, {'face': 'doublewhiteshield-purple.png', 'numOfFaces': 1}, {'face': 'blackshield-purple.png', 'numOfFaces': 1}]
            },
            'black': {
            	'maxNumberOfDiceType': None,
                'faces': [{'face': 'skull-black.png', 'numOfFaces': 4}, {'face': 'whiteshield-black.png', 'numOfFaces': 1}, {'face': 'blackshield-black.png', 'numOfFaces': 1}]
            },
            'yellow': {
            	'maxNumberOfDiceType': None,
                'faces': [{'face': 'skull-yellow.png', 'numOfFaces': 1}, {'face': 'doubleskull-yellow.png', 'numOfFaces': 1}, {'face': 'whiteshield-yellow.png', 'numOfFaces': 1}, {'face': 'doublewhiteshield-yellow.png', 'numOfFaces': 1}, {'face': 'blackshield-yellow.png', 'numOfFaces': 1}, {'face': 'doubleblackshield-yellow.png', 'numOfFaces': 1}]
            }
        }
    },
    'scdice': {
        'name': 'Space Crusade',
        'maxNumberOfTotalDice': 8,
        'imageDirectory': 'spacecrusade',
        'regex': r'^(\d{1,2}\s[a-zA-Z]+\b\s?)+$',
        'usage': 'Usage:\n  **_!scdice # color_** to roll dice, multiple numbers and colors are accepted. (Ex. **_!scdice 2 red 2 black_**)',
        'help': 'h**Roll Space Crusade combat dice**:\n \
To roll Space Crusade dice use the _**!scroll**_ or _**!sqroll**_ command followed by the \
number of dice you wish to roll, followed by the color you wish to roll. In Space Crusade \
you can roll up to 4 white and up to 4 red dice.\n \
**Examples:** _**!scroll 2 white**, **!scroll 1 red 3 white**, **!sqroll 1 white 2 red**_',
        'defaultDiceType': None,
        'diceTypes': {
            'white': {
                    'maxNumberOfDiceType': 4,
                    'faces': [{'face': 'white-1.png', 'numOfFaces': 1}, {'face': 'white-2.png', 'numOfFaces': 1}, {'face': 'white-0.png', 'numOfFaces': 4}]
            },
            'red': {
                    'maxNumberOfDiceType': 4,
                    'faces': [{'face': 'red-1.png', 'numOfFaces': 1}, {'face': 'red-2.png', 'numOfFaces': 1}, {'face': 'red-3.png', 'numOfFaces': 1}, {'face': 'red-0.png', 'numOfFaces': 3}]
            }
        }
    },
    'descentdice': {
        'name': 'Descent 2nd Ed.',
        'maxNumberOfTotalDice': 10,
        'imageDirectory': 'descent',
        'regex': r'^(\d{1,2}\s[a-zA-Z]+\b\s?)+$',
        'help': '**Roll Descent 2nd Edition combat dice**:\n \
To roll Descent dice use the _**!descentroll**_ or _**!descentdice**_ command followed by the \
number of dice you wish to roll, followed by the color you wish to roll. In the Descent 2e \
board game you can roll up to 2 red, 1 blue, 2 yellow, 1 brown, 2 gray/grey, and 1 black dice.\n \
**Examples:** _**!descentdice 2 red**, **!descentdice 2 red 1 blue**, **!descentdice 1 brown 1 gray**_',
        'defaultDiceType': None,
        'diceTypes': {
            'red': {
                'maxNumberOfDiceType': 2,
                'faces': [{'face': 'red-1heart.png', 'numOfFaces': 1}, {'face': 'red-2hearts.png', 'numOfFaces': 3}, {'face': 'red-3hearts.png', 'numOfFaces': 1}, {'face': 'red-3hearts-1surge.png', 'numOfFaces': 1}]
            },
            'blue': {
                'maxNumberOfDiceType': 1,
                'faces': [{'face': 'blue-miss.png', 'numOfFaces': 1}, {'face': 'blue-number2-2hearts-1surge.png', 'numOfFaces': 1}, {'face': 'blue-number3-2hearts.png', 'numOfFaces': 1}, {'face': 'blue-number4-2hearts.png', 'numOfFaces': 1}, {'face': 'blue-number5-1heart.png', 'numOfFaces': 1}, {'face': 'blue-number6-1heart-1surge.png', 'numOfFaces': 1}]
            },
            'yellow': {
                'maxNumberOfDiceType': 2,
                'faces': [{'face': 'yellow-2hearts.png', 'numOfFaces': 1}, {'face': 'yellow-1heart-1surge.png', 'numOfFaces': 1}, {'face': 'yellow-number1-1heart.png', 'numOfFaces': 1}, {'face': 'yellow-number1-1surge.png', 'numOfFaces': 1}, {'face': 'yellow-number2-1heart.png', 'numOfFaces': 1}, {'face': 'yellow-2hearts-1surge.png', 'numOfFaces': 1}]
            },
            'brown': {
                    'maxNumberOfDiceType': 1,
                    'faces': [{'face': 'brown-blank.png', 'numOfFaces': 3}, {'face': 'brown-1shield.png', 'numOfFaces': 2}, {'face': 'brown-2shields.png', 'numOfFaces': 1}]
            },
            'gray': {
                'maxNumberOfDiceType': 2,
                'faces': [{'face': 'gray-blank.png', 'numOfFaces': 1}, {'face': 'gray-1shield.png', 'numOfFaces': 3}, {'face': 'gray-2shields.png', 'numOfFaces': 1}, {'face': 'gray-3shields.png', 'numOfFaces': 1}]
            },
            'black': {
                'maxNumberOfDiceType': 1,
                'faces': [{'face': 'black-blank.png', 'numOfFaces': 1}, {'face': 'black-2shields.png', 'numOfFaces': 3}, {'face': 'black-3shields.png', 'numOfFaces': 1}, {'face': 'black-4shields.png', 'numOfFaces': 1}]
            }
        }
    },
    'doomdice': {
        'name': 'DOOM 2016 Board Game',
        'maxNumberOfTotalDice': 6,
        'imageDirectory': 'doom',
        'regex': r'^(\d{1,2}\s[a-zA-Z]+\b\s?)+$',
        'help': '**Roll DOOM (2016) board game combat dice**:\n \
To roll DOOM dice use the _**!doomroll**_ or _**!doomdice**_ command followed by the \
number of dice you wish to roll, followed by the color you wish to roll. In the DOOM 2016 \
board game you can roll up to 4 red and up to 2 black dice.\n \
**Examples:** _**!doomdice 2 red**, **!doomdice 2 red 2 black**, **!doomdice 1 red 3 black**_',
        'defaultDiceType': None,
        'diceTypes': {
            'red': {
                'maxNumberOfDiceType': 4,
                'faces': [{'face': 'red-blank.png', 'numOfFaces': 1}, {'face': 'red-1shot.png', 'numOfFaces': 3}, {'face': 'red-2shots.png', 'numOfFaces': 2}]
            },
            'black': {
                'maxNumberOfDiceType': 2,
                'faces': [{'face': 'black-1shot.png', 'numOfFaces': 2}, {'face': 'black-2shots.png', 'numOfFaces': 3}, {'face': 'black-3shots.png', 'numOfFaces': 1}]
            }
        }
    },
    'drgdice': {
        'name': 'Deep Rock Galactic Board Game',
        'maxNumberOfTotalDice': 3,
        'imageDirectory': 'drg',
        'regex': r'^(\d{1,2}\s[a-zA-Z]+\b\s?)+$',
        'help': '**Deep Rock Galactic board game dice**:\n \
To roll Deep Rock Galactic dice use the _**!drgroll**_ or _**!drgdice**_ command followed by the \
number of dice you wish to roll, followed by the color you wish to roll. In the DRG \
board game you can roll up to 2 red, 2 blue, 3 yellow, 3 green, 1 gray/grey, 2 white, and 2 black dice.\n \
**Examples:** _**!drgdice 2 yellow**, **!drgdice 2 red**, **!drgdice 3 green**_',
        'defaultDiceType': None,
        'diceTypes': {
            'red': {
                'maxNumberOfDiceType': 2,
                'faces': [{'face': 'red-1explosion.png', 'numOfFaces': 3}, {'face': 'red-2explosions.png', 'numOfFaces': 2}, {'face': 'red-movecreature.png', 'numOfFaces': 1}]
            },
            'blue': {
                'maxNumberOfDiceType': 2,
                'faces': [{'face': 'blue-1piercing.png', 'numOfFaces': 3}, {'face': 'blue-2piercing.png', 'numOfFaces': 2}, {'face': 'blue-blank.png', 'numOfFaces': 1}]
            },
            'yellow': {
                'maxNumberOfDiceType': 3,
                'faces': [{'face': 'yellow-1flame.png', 'numOfFaces': 3}, {'face': 'yellow-2flames.png', 'numOfFaces': 1}, {'face': 'yellow-blank.png', 'numOfFaces': 2}]
            },
            'green': {
                'maxNumberOfDiceType': 3,
                'faces': [{'face': 'green-bullet.png', 'numOfFaces': 4}, {'face': 'green-blank.png', 'numOfFaces': 2}]
            },
            'gray': {
                'maxNumberOfDiceType': 1,
                'faces': [{'face': 'gray-gold.png', 'numOfFaces': 2}, {'face': 'gray-nitra.png', 'numOfFaces': 2}, {'face': 'gray-blank.png', 'numOfFaces': 2}]
            },
            'white': {
                'maxNumberOfDiceType': 2,
                'faces': [{'face': 'white-1pickaxe.png', 'numOfFaces': 3}, {'face': 'white-2pickaxes.png', 'numOfFaces': 2}, {'face': 'white-blank.png', 'numOfFaces': 1}]
            },
            'black': {
                'maxNumberOfDiceType': 2,
                'faces': [{'face': 'black-damage.png', 'numOfFaces': 3}, {'face': 'black-specialeffect.png', 'numOfFaces': 2}, {'face': 'black-blank.png', 'numOfFaces': 1}]
            }
        }
    }
}

## print the entire faces list for each type of dice
#for diceType in dice['hqdice']['diceTypes'].keys():
#	print (dice['hqdice']['diceTypes'][diceType]['faces'])
#    
##  print the individual faces for a given die
#	for diceFace in dice['hqdice']['diceTypes'][diceType]['faces']:
#		print (diceFace)

## print the available colors for a given game's dice
#for diceColor in dice['hqdice']['diceTypes']:
#   print (diceColor)



