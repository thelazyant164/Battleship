#Import modules and libraries
from random import randint

#Define board mapping function
def mapBoard(col, row, value):
    board = [[value for x in range(col)] for y in range(row)]
    return board

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

#Define function to randomly generate listOfShip
#Possible ship generation: 2 - 4 types of ship, possible length: 2 - 6, num of same ship type: 1 - 4
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

#Define sink function
def sink(board, playerBoard, winScore, score):
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
    viewBoard(playerBoard)
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

#DEBUG

#DEBUG: Instantiate board with custom rows and columns
"""board = mapBoard(7, 7)"""
#mapBoard(dimension, dimension)

#DEBUG: Instantiate list of ships to be randomly spawned on board
""" listOfShip = [
    [[1, 2], 2],
    [[1, 1], 2],
    [[1, 3], 1]
] """
#listOfShip = [shipType1, shipType2...]
              #ShipType = [shipSize, numOfShip]
                          #shipSize = [shipSizeInRow, shipSizeInCol]
                          #Warning: valid listOfShip has sum of shipDimension x numOfShip <= boardDimension

#DEBUG: view board creation
"""viewBoard(board)"""

#Replay loop
replay = True
while (replay):

    #Instantiate level

    #Instantiate random map
    dimension = randint(7, 9)
    board = mapBoard(dimension, dimension, 'O')
    playerBoard = mapBoard(dimension, dimension, '?')

    #Instantiate random list of ships
    listOfShip = createList(board)

    #Randomly spawn ships on map
    mapShip(board, listOfShip)

    #Initialize variables
    win = False
    hit = 0
    lim = int(dimension ** 2 / 1.5)
    score = 0
    
    #Determine winning condition
    winScore = winCond(listOfShip)

    #Title screen
    #Page break
    print("\n\n\n\n\n\n")
    print(f"Welcome to a game of Battleship!\n\nYour primary objective is to torpedo the fuselage and sink all {winScore} of the enemies' ships on a {dimension}x{dimension} grid.\n\nLet's begin!\n\n\n")

    #Preview board
    viewBoard(playerBoard)

    #Symbol
    print("\n\n? : uncharted\n")
    print("  : empty\n")
    print("X : hit\n")
    print("F : fuselage\n")

#Game loop
    while (hit < lim):
        print(f"\n\nYou have {lim - hit} torpedoes left.\n\n")
        score += sink(board, playerBoard, winScore, score)
        hit += 1

        #Win
        if (score >= winScore):
            print("\n\nCongratulations! You have sunk all of the enemies' ships!\n\n")
            print(f"You sank all {winScore} ships!\n\n")
            win = True
            break
    
    #Lose
    if (not win):
        print("\n\nYou've used up all of your torpedoes. Game over!\n\n")
        print(f"You sank a total of {score} ships.\nTo win, you need to sink all {winScore} ships.\n\n")
    
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