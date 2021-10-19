#Import libraries and functions
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

#Define function to plan new ship placement
def planNewPlacement(board, shipSize):
    boardRow = len(board)
    boardCol = len(board[0])
    planBoard = mapBoard(boardCol, boardRow, 'O')
    y = shipSize[0]
    x = shipSize[1]
    startingPointCoordY = randint(0, boardRow - y)
    startingPointCoordX = randint(0, boardCol - x)
    planBoard[startingPointCoordY][startingPointCoordX] = "?"
    if (x > 1):
        for x1 in range(startingPointCoordX, startingPointCoordX + x):
            planBoard[startingPointCoordY][x1] = "?"
    elif (y > 1):
        for y1 in range(startingPointCoordY, startingPointCoordY + y):
            planBoard[y1][startingPointCoordX] = "?"
    return planBoard

#Define function to verify and undo or finalize ship placement
def verifyPlacement(board, planBoard):
    boardRow = len(board)
    boardCol = len(board[0])
    checkList = []
    for row in range(0, boardRow):
        for col in range(0, boardCol):
            if (board[row][col] == "O" and planBoard[row][col] == "?"):
                listTemp = []
                listTemp.append(row)
                listTemp.append(col)
                checkList.append(listTemp)
            elif (board[row][col] == "O" and planBoard[row][col] == "O"):
                continue
            elif (board[row][col] == "X" and planBoard[row][col] == "O"):
                continue
            elif (board[row][col] == "X" and planBoard[row][col] == "?"):
                return False
    #Define algorithm to assign 1 hitbox of each ship as kill spot
    fuselage = randint(1, len(checkList))
    i = 1
    for unmarked in checkList:
        board[unmarked[0]][unmarked[1]] = "X"
        if (i == fuselage):
            board[unmarked[0]][unmarked[1]] = "F"
        i += 1
    return True
    
#Define function to map ship
def mapShip(board, listOfShip):
    for shipType in listOfShip:
        numOfShipToCreate = shipType[1]
        shipSize = shipType[0]
        for i in range(numOfShipToCreate):
            verified = False
            while (not verified):
                planBoard = planNewPlacement(board, shipSize)
                verified = verifyPlacement(board, planBoard)
    return board

#Define function to plot player's ship placement
def arrangeShip(hiddenBoard, listOfShip):
    print(f'Let\'s get to know your own armada first. You have a total of {len(listOfShip)} types of ships:\n')
    for shipType in listOfShip:
        print(f'- {shipType[1]} {shipType[0][0]}x{shipType[0][1]}')
    print('\nRemember, each ship can only be placed horizontally or vertically, and must be positioned within the boundaries of the board.')
    print('Plot out your ship placement carefully, because once a ship has moved into position, it shall become static for the entire extent of the battle.')
    print('Let\'s begin plotting your own ship placement!\n')
    viewBoard(hiddenBoard)
    for shipType in listOfShip:
        for numOfShip in range(shipType[1]):
            invalid = True
            while (invalid):
                try:
                    x, y = input(f'\nWhere should the furthermost Northwest block of this {shipType[0][0]}x{shipType[0][1]} ship be placed?\n(column : row): ').split(':')
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

#Define sink function
def sink(board, playerBoard, winScore, score):
    viewBoard(playerBoard)
    tempscore = 0
    dimension = len(board)
    invalid = True
    while (invalid):
        print("\n\nWhere do you want to sink?\n\n")
        try:
            x, y = input(f'Where do you want to sink? (1 - {str(dimension)})\n(Column : Row) ').split(':')
            x = int(x) - 1
            y = int(y) - 1
            if (playerBoard[y][x] != '?' or x < 0 or y < 0): raise ValueError
        except (ValueError, UnboundLocalError, IndexError):
            print('\nInvalid input detected. Please try again.\n')
            continue
        else:
            invalid = False
            if (board[y][x] == "X"):
                playerBoard[y][x] = "X"
                print(f"\n\nCongratulations. {x + 1}:{y + 1} was a direct hit.\nTry checking the area nearby for fuselage...?\n\n")
            elif (board[y][x] == "F"):
                tempscore += 1
                playerBoard[y][x] = "F"
                print(f"\n\nCongratulations. {x + 1}:{y + 1} was a fuselage. Due to that, an entire ship has been sunken.\n{winScore - score - tempscore} ships remaining from total annihilation of the enemy's fleet.\n\n")    
            else:
                playerBoard[y][x] = " "
                print(f"\n\nUnfortunately, {x + 1}:{y + 1} was a miss.\n\n")
    return tempscore

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

#Generate answer board
def answer(board, playerBoard):
    boardRow = len(board)
    boardCol = len(board[0])
    answerBoard = mapBoard(boardCol, boardRow, 'O')
    for row in range(0, len(board)):
        for col in range(0, len(board[0])):
            if (board[row][col] == "O"):
                answerBoard[row][col] = " "
            elif (board[row][col] == playerBoard[row][col] == "X"):
                answerBoard[row][col] = "V"
            elif (board[row][col] == "X" != playerBoard[row][col]):
                answerBoard[row][col] = "X"
            elif (board[row][col] == "F" != playerBoard[row][col]):
                answerBoard[row][col] = "F"
            else:
                answerBoard[row][col] = "O"
    return answerBoard

#Replay loop
replay = True
while (replay):

    #Instantiate level

    #Instantiate random map
    dimension = randint(7, 9)
    board = mapBoard(dimension, dimension, 'O')
    playerBoard = mapBoard(dimension, dimension, '?')
    hiddenBoard = mapBoard(dimension, dimension, ' ')
    computerBoard = mapBoard(dimension, dimension, '?')

    #Instantiate random list of ships
    listOfShip = createList(board)

    #Randomly spawn ships on map
    mapShip(board, listOfShip)

    #Initialize variables
    lim = int(dimension ** 2 / 1.5)
    playerScore = 0
    computerScore = 0
    
    #Determine winning condition
    winScore = winCond(listOfShip)

    #Title screen
    #Page break
    print("\n\n\n\n\n\n")
    print(f"Welcome to a game of Battleship!\n\nYour goal is to torpedo the fuselages and sink all {winScore} of the enemies' ships on a {dimension}x{dimension} grid.\nHowever, the enemy admiral will be attempting to do the same with your armada of ships.\nYou will each take turn shooting down your opponent, the number of torpedoes you have each round will be represented by the number of ships that your opponent have yet to discover.\nRemember, unless a torpedo directly strikes a fuselage, your ship won't explode, but the resulting seismic feedback will alert the enemy's admiral of your ship's whereabouts.\n\nLet's begin!\n\n\n")

    #Request player to manually plot out ship placement
    arrangeShip(hiddenBoard, listOfShip)

    #Preview board
    viewBoard(playerBoard)

    #Symbol
    print("\n\n? : uncharted\n")
    print("  : empty\n")
    print("X : hit\n")
    print("F : fuselage\n")

    #Game loop
    continuePlaying = True
    while (continuePlaying):

        for i in range(winScore - computerScore):
            print(f'{winScore - computerScore - i} torpedoes left this round.')
            playerScore += sink(board, playerBoard, winScore, playerScore)
            viewBoard(playerBoard)
                
            #Win
            if (playerScore >= winScore):
                print("\n\nCongratulations! You have sunk all of the enemies' ships!\n\n")
                print('Game over!')
                continuePlaying = False
                break
            
        for i in range(winScore - playerScore):
            print(f'{winScore - playerScore - i} torpedoes left this round.')
            computerScore += computerSink(hiddenBoard, computerBoard, winScore, computerScore)
        
            #Lose
            if (computerScore >= winScore):
                print("\n\nOh dear! All of your ships have been sunk!\n\n")
                print('Game over!')
                continuePlaying = False
                break
    
    #Show board prompt
    choice = input("\n\nDo you want to view the asnwer?\n(y) for yes, (n) for no.\n\n")
    if (choice == "y"):
        showBoard = True
    else:
        showBoard = False

    if (showBoard):
        answerBoard = answer(board, playerBoard)

        #Symbol
        print("\n\nX : uncharted ship segment\n")
        print("  : empty\n")
        print("V : found ship segment\n")
        print("O : found fuselage\n")
        print("F : uncharted fuselage\n")

        viewBoard(answerBoard)

    #Replay prompt
    choice = input("\n\nDo you want to replay?\n(y) for yes, (n) for no.\n\n")
    if (choice == "y"):
        replay = True
    else:
        replay = False