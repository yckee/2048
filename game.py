import numpy as np
from random import randint

def newGame(size=4):
    empty = np.zeros((size,size), dtype=np.int)
    return fillCell(empty)

def fillCell(game):
    # fills a random empty cell with 2
    # takes an array, returns an array with a random empty cell filled
    size = len(game)
    emptycells = []
    # the loop gets a list of empty cells
    for row in range(size):
        for col in range(size):
            if game[row][col] == 0:
                emptycells.append([row, col])
    # check if there are empty cells
    if emptycells:
        # uses randint to get a random index from the list of empty cells
        celltofill = emptycells[randint(0, len(emptycells)-1)]
        r, c = celltofill
        # gets a distribution with 10% chance of 4
        distribution = [2 for i in range(9)]
        distribution.append(4)
        num = np.random.choice(np.array(distribution))
        # fills the cell with 2 or 4
        game[r][c] = num
        return game
    else:
        # case when no empty cells
        return


def gameOver(game):
    # checks if there are any possible moves left
    if np.all(game):
        # check that there are no empty cells
        can_merge = False
        size = len(game)
        # check if can merge with cell on the right
        for r in range(size):
            for c in range(size-1):
                if game[r][c] == game[r][c+1]:
                    can_merge = True
        #check if can merge with cell below
        for r in range(size-1):
            for c in range(size):
                if game[r][c] == game[r+1][c]:
                    can_merge = True
    # if there are empty cells, return gameover = False
    else:
        return False
    
    if can_merge == True:
        return False
    else:
        return True

def mergeCells(rc,direction):
    # first argument is a row/col as a 1d array,
    # second argument can be "left","right","up" or "down"
    # effect of "left" and "up" is the same, "right" and "down" also
    # finds cells to merge and returns the row/col as an array
    if direction == "right" or direction == "down":
        rc = rc[::-1]
    
    if not np.all(rc):
        # if there are zeros, shifts all the zeros to the right
        nonzero_elements = []
        for i in range(len(rc)):
            if rc[i] != 0:
                nonzero_elements.append(rc[i])
        zeros = len(rc)-len(nonzero_elements)
        for extra in range(zeros):
            nonzero_elements.append(0)
        rc = np.array(nonzero_elements)
    
    # find adjacent cells that are the same and merge
    for i in range(1, len(rc)):
        if rc[i] == rc[i-1] and rc[i] != 0:
            rc[i-1] *= 2
            rc[i] = 0
    # shift all the zeros to the right again
    if not np.all(rc):
        nonzero_elements = []
        for i in range(len(rc)):
            if rc[i] != 0:
                nonzero_elements.append(rc[i])
        zeros = len(rc)-len(nonzero_elements)
        for extra in range(zeros):
            nonzero_elements.append(0)
        rc = np.array(nonzero_elements)
    if direction == "right" or direction == "down":
        return rc[::-1]
    else:
        return rc


def userMove(game, key):
    # moves the numbers according to the keys pressed
    # returns the new game array
    oldgame = game
    size = len(game)
    if key == "up" or key == "down":
        newgame = []
        for col in range(size):
            # uses slicing to get each column
            a = game[:, col]  # a is a column
            newcol = mergeCells(a, key)
            newgame.append(newcol)
        return np.array(newgame).T
    elif key == "left" or key == "right":
        newgame = []
        for row in range(size):
            a = game[row]
            newrow = mergeCells(a,key)
            newgame.append(newrow)
        return np.array(newgame)


a = newGame()
while not gameOver(a):
    print(a)
    char = input("Please press a key")
    if char == "w":
        key = "up"
    elif char == "s":
        key = "down"
    elif char == "a":
        key = "left"
    elif char == "d":
        key = "right"
    a = userMove(a, key)
    fillCell(a)
else:
    print("gameover!")