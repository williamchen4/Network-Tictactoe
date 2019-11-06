def printBoard(state):
    takenSpaces = state["takenSpaces"]

    output = "\n"
    index = 0
    output += "-------\n"
    for row in range(3):
        for column in range(0,3):
            output += "|"
            if takenSpaces[index] == False:
                output += " "
            else:
                output += takenSpaces[index]
            index += 1
        output += "|\n"
        output += "-------\n"
    return output

def isGameOver(state):
    takenSpaces = state["takenSpaces"]
    message = "Game Over: "
    # rows
    for x in [0,3,6]:
        if takenSpaces[x] and takenSpaces[x] == takenSpaces[x+1] and takenSpaces[x+1] == takenSpaces[x+2]:
            return message + takenSpaces[x] + " won"
    # columns
    for x in [0,1,2]:
        if takenSpaces[x] and takenSpaces[x] == takenSpaces[x+3] and takenSpaces[x+3] == takenSpaces[x+6]:
            return message + takenSpaces[x] + " won"
    # diagonals
    if takenSpaces[4]:
        if takenSpaces[0] == takenSpaces[4] and takenSpaces[4] == takenSpaces[8] or \
        takenSpaces[2] == takenSpaces[4] and takenSpaces[4] == takenSpaces[6]:
            return message + takenSpaces[4] + " won"
    # draw
    if all(takenSpaces):
        return message + "Draw"
    return False

def getNewPlayer(symbol):
    return {
        "takenSpaces": [False, False, False, False, False, False, False, False, False],
        "player": symbol
    }

def userInputValid(takenSpaces, space):
    try:
        space = int(space)
        if space < 0 or space > 9 or takenSpaces[space] != False:
            return False
        return True
    except:
        return False

def userTurn(state):
    takenSpaces = state["takenSpaces"]
    space = input("Enter number of cell: ")
    while(not userInputValid(takenSpaces, space)):
        space = input("Invalid. Enter number of cell: ")

    state["takenSpaces"][int(space)] = state["player"]
    return state

def computerTurn(state):
    takenSpaces = state["takenSpaces"]
    for x in range(9):
        if takenSpaces[x] == False:
            state["takenSpaces"][x] = "O"
            return state
