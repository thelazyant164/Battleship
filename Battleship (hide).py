#Import modules and libraries
from random import randint

#Define functions

#Define board mapping function
def mapBoard(col, row, value):
    board = [[value for x in range(col)] for y in range(row)]
    return board

#Define board mapping function
def mapMetaBoard(col, row):
    metaboard = [[0 for x in range(col)] for y in range(row)]
    return metaboard

#Define view board function
def viewBoard(board):
    col = len(board[0])
    row = len(board)
    border = ""
    topBorder = "#||"
    for i in range(0, col):
        border += "_" * 2
        topBorder += str(i + 1)
        topBorder += " "
    border += "___"
    print(topBorder)
    print(border)
    for i in range(0, row):
        print(str(i + 1) + "||" + " ".join(board[i]) + "|")

#Define function to randomly generate listOfShip
#Possible ship generation: 2 - 4 types of ship, possible length: 2 - 6, num of same ship type: 1 - 4
#listOfShip = [shipType1, shipType2...]
    #shipType = [shipSize, numOfShip]
    #shipSize = [shipSizeInRow, shipSizeInCol]
    #Warning: valid listOfShip has sum of shipDimension x numOfShip <= boardDimension
def createList(board):
    boardDimension = len(board) * len(board[0])
    verified = False
    while (not verified):
        listOfShip = []
        verifier = 0
        numOfShipType = 4
        for i in range(numOfShipType):
            list = []
            tempList = []
            if (randint(1,2) == 1):
                shipSizeInRow = 1
                shipSizeInCol = randint(2, 6)
            else:
                shipSizeInCol = 1
                shipSizeInRow = randint(2, 6)
            numOfShip = randint(1, 4)
            tempList.append(shipSizeInRow)
            tempList.append(shipSizeInCol)
            list.append(tempList)
            list.append(numOfShip)
            listOfShip.append(list)
            verifier += shipSizeInRow * shipSizeInCol * numOfShip
        verified = verifier <= boardDimension/3 and verifier >= boardDimension/4
    return listOfShip

#Define function to plot player's ship placement
def arrangeShip(hiddenBoard, listOfShip):
    print(f'Let\'s get to know your own armada first. You have a total of {len(listOfShip)} types of ships:\n')
    for shipType in listOfShip:
        print(f'- {shipType[1]} {shipType[0][0]}x{shipType[0][1]}')
    print('\nPlot out your ship placement carefully, because once a ship has moved into position, it shall become static for the entire extent of the battle.')
    print('\nLet\'s begin plotting your own ship placement!\n')
    viewBoard(hiddenBoard)
    for shipType in listOfShip:
        for numOfShip in range(shipType[1]):
            invalid = True
            while (invalid):
                try:
                    x, y = input(f'\nWhere should this {shipType[0][0]}x{shipType[0][1]} ship be placed?\n(column : row): ').split(':')
                    orientation = input('Horizontal (h) or vertical (v)? ')
                    x = int(x) - 1
                    y = int(y) - 1
                    fx, fy = input(f'Where should its fuselage be?\n(column : row): ').split(':')
                    fx = int(fx) - 1
                    fy = int(fy) - 1
                    if (min(x, y, fx, fy) < 0): raise ValueError
                    if (orientation not in ['h', 'v']): raise TypeError
                    if (orientation == 'h'):
                        if (fy != y): raise ValueError
                        row = y
                        valid = 0
                        for col in range(x, x + max(shipType[0])):
                            if (hiddenBoard[row][col] != ' '): raise ValueError
                            if (col == fx): valid += 1
                        if (valid == 0): raise ValueError
                        for col in range(x, x + max(shipType[0])):
                            hiddenBoard[row][col] = 'X'
                        for col in range(x, x + max(shipType[0])):    
                            if (row == fy and col == fx):
                                hiddenBoard[row][col] = 'F'
                                invalid = False
                    else:
                        if (fx != x): raise ValueError
                        col = x
                        valid = 0
                        for row in range(y, y + max(shipType[0])):
                            if (hiddenBoard[row][col] != ' '): raise ValueError
                            if (row == fy): valid += 1
                        if (valid == 0): raise ValueError
                        for row in range(y, y + max(shipType[0])):
                            hiddenBoard[row][col] = 'X'
                        for row in range(y, y + max(shipType[0])):    
                            if (row == fy and col == fx):
                                hiddenBoard[row][col] = 'F'
                                invalid = False
                except (IndexError, TypeError, ValueError):
                    print('Invalid placement. Please try again.')
            viewBoard(hiddenBoard)
    return hiddenBoard

#AI
#Define computer's turn
def computerSink(hiddenBoard, computerBoard, winScore, score):
    tempscore = 0
    print("\n\nThe enemy's admiral is planning a torpedo strike...\n\n")
    input('Press any key to continue...')
    invalid = True
    while (invalid):

        def decide(hiddenBoard, computerBoard):
            def sweep(metaboard):
                dimension = len(metaboard)
                updated = True
                while (updated):
                    update = 0
                    for row in range(dimension):
                        for col in range(dimension):
                            if (metaboard[row][col] == 'X'):
                                metaboard[row][col] = 'O'
                                try:
                                    if (col - 1 < 0): raise IndexError
                                    if isinstance(metaboard[row][col - 1], int):
                                        metaboard[row][col - 1] += 1
                                        update += 1
                                except IndexError: pass
                                try:
                                    if (row - 1 < 0): raise IndexError
                                    if isinstance(metaboard[row - 1][col], int):
                                        metaboard[row - 1][col] += 1
                                        update += 1
                                except IndexError: pass
                                try:
                                    if (row + 1 < 0): raise IndexError
                                    if isinstance(metaboard[row + 1][col], int):
                                        metaboard[row + 1][col] += 1
                                        update += 1
                                except IndexError: pass    
                                try:
                                    if (col + 1 < 0): raise IndexError
                                    if isinstance(metaboard[row][col + 1], int):
                                        metaboard[row][col + 1] += 1
                                        update += 1
                                except IndexError: pass    
                    if (update > 0): updated = True
                    else: updated = False
                
            def pick(metaboard):
                dimension = len(metaboard)
                consider = []
                for row in range(dimension):
                    for col in range(dimension):
                        if (isinstance(metaboard[row][col], int)): consider.append(metaboard[row][col])
                value = max(consider)
                if (value == 0):
                    x = randint(1, dimension) - 1
                    y = randint(1, dimension) - 1
                else:
                    for row in range(dimension):
                        for col in range(dimension):
                            if (metaboard[row][col] == value):
                                x = col
                                y = row
                return x, y    

            dimension = len(hiddenBoard)
            metaboard = mapMetaBoard(dimension, dimension)
            for row in range(dimension):
                for col in range(dimension):
                    if (computerBoard[row][col] in ['X', 'F', ' ']): metaboard[row][col] = computerBoard[row][col]
            sweep(metaboard)
            x, y = pick(metaboard)
            return x, y

        x, y = decide(hiddenBoard, computerBoard)
        if (computerBoard[y][x] != '?'):
            invalid = True
        else:
            invalid = False
            if (hiddenBoard[y][x] == "X"):
                print(f'Fire! The enemy\'s admiral chose to shoot at {x + 1}:{y + 1}.')
                computerBoard[y][x] = "X"
                print(f"\n\nOh no! The torpedo exploded upon impact against the metallic hull of the battleship, alarming the admiral of its location.\nThe admiral will be on to it now.\n\n")
            elif (hiddenBoard[y][x] == "F"):
                print(f'Fire! The enemy\'s admiral chose to shoot at {x + 1}:{y + 1}.')
                tempscore += 1
                computerBoard[y][x] = "F"
                print(f"\n\nOh no! They hit a fuselage and took down an entire ship!.\n{winScore - score - tempscore} ships remaining.\n\n")    
            else:
                print(f'Fire! The enemy\'s admiral chose to shoot at {x + 1}:{y + 1}.')
                computerBoard[y][x] = " "
                print(f"\n\nFortunately, your ship was located elsewhere, and thus elluded the assault intact.\n\n")
    viewBoard(computerBoard)
    return tempscore

#Determine winning condition
def winCond(listOfShip):
    victoryWinScore = 0
    for typeOfShip in listOfShip:
        victoryWinScore += typeOfShip[1]
    return victoryWinScore

#Replay loop
replay = True
while (replay):

    #Instantiate level

    #Instantiate random map
    dimension = randint(7, 9)
    hiddenBoard = mapBoard(dimension, dimension, ' ')
    computerBoard = mapBoard(dimension, dimension, '?')

    #Instantiate random list of ships
    listOfShip = createList(hiddenBoard)

    #Initialize variables
    hit = 0
    lim = int(dimension ** 2 / 1.5)
    score = 0
    
    #Determine winning condition
    winScore = winCond(listOfShip)

    #Title screen
    #Page break
    print("\n\n\n\n\n\n")
    print(f"Welcome to a game of Battleship!\n\nThe enemy's naval fleet has decided to launch an assault on your armada of ships!\nYour primary objective is to hide all {winScore} fuselages of your ships away from {lim} of their torpedoes on a {dimension}x{dimension} grid.\nRemember, unless a torpedo directly strikes a fuselage, your ship won't explode, but the resulting seismic feedback will alert the enemy's admiral of your ship's whereabouts.\n\nLet's begin!\n\n\n")

    #Request player to manually plot out ship placement
    arrangeShip(hiddenBoard, listOfShip)

    #Symbol
    print("\n\n? : uncharted\n")
    print("  : empty\n")
    print("X : hit\n")
    print("F : fuselage\n")

#Game loop
    while (hit < lim):
        print(f"\n\nThe enemy has {lim - hit} torpedoes left.\n\n")
        score += computerSink(hiddenBoard, computerBoard, winScore, score)
        hit += 1

        #Lose
        if (score >= winScore):
            print("\n\nOh dear! All of your ships have been sunk!\n\n")
            lose = True
            break
        else:
            lose = False
    
    #Win
    if (not lose):
        print("\n\nThey've used up all of their torpedoes. You win!\n\n")
        print(f"You started out with {winScore} ships.\nSo far, {score} ships have been sunk.\n{winScore - score} of your ships survived the assault, thanks to your ingenuity!\n\n")

    #Replay prompt
    choice = input("\n\nDo you want to replay?\n(y) for yes, (n) for no.\n\n")
    if (choice == "y"):
        replay = True
    else:
        replay = False