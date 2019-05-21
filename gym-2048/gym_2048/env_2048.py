import gym
import numpy as np
import os
from random import randint
from colorama import init

 
class Env_2048(gym.Env):  
    metadata = {'render.modes': ['human']}   
    
    def __init__(self, size=4):
        self.size = size
        board = self.__fillCell(np.zeros((self.size,self.size), dtype = np.int))
        self.board = self.__fillCell(board)
        self.score = 0
        self.clear = lambda: os.system('cls' if os.name=='nt' else 'clear')
        

    def step(self, action):
        reward = 0
        oldboard = self.board
        if action == 'u' or action == 'd':
            newboard = []
            for col in range(self.size):
                newcol, gainedscore = self.__mergeCells(self.board[:, col],action)
                newboard.append(newcol)
                reward += gainedscore
            self.board = np.array(newboard).T
        elif action == 'l' or action == 'r':
            newboard = []
            for row in range(self.size):
                newrow, gainedscore = self.__mergeCells(self.board[row], action)
                newboard.append(newrow)
                reward += gainedscore
            self.board = np.array(newboard)
        self.score += reward
        if np.any(oldboard != self.board) : 
            self.board = self.__fillCell(self.board)
        else: 
            reward = -50
        return self.board, reward, self.__gameOver(),{}

 
    def reset(self):
        board = self.__fillCell(np.zeros((self.size,self.size), dtype = np.int))
        self.board = self.__fillCell(board)
        self.score = 0
        return self.board
 
    def render(self, mode='human', close=False):
        init()
        self.clear()
        colors ={
            0: 47,
            2: 42,
            4: 42,
            8: 42,
            16: 41,
            32: 41,
            64: 41,
            128: 43,
            256: 43,
            512: 43,
            1024: 43,
            2048: 46
        }
        width = len(str(np.max(self.board)))
        dash = '-'*((width+1)*self.size + self.size-1)
        print(dash+ '\n \x1b[6;31;40m' + f'Score = {self.score} \n' + '\x1b[0m')
        for row in self.board:
            print ("|".join(("\x1b[6;30;%sm %*s"+'\x1b[0m') % (str(colors.get(n,46)),width, str(n)) for n in row))
            print(dash)

    def __fillCell(self,board):
        """ Fill a random empty cell with 2 or 4 """
        
        emptycells = []
        # the loop gets a list of empty cells
        for row in range(self.size):
            for col in range(self.size):
                if board[row][col] == 0:
                    emptycells.append([row, col])
        # check if there are empty cells
        if emptycells:
            # uses randint to get a random index from the list of empty cells
            rowtofill, coltofill = emptycells[randint(0, len(emptycells)-1)]
            # gets a distribution with 10% chance of 4
            distribution = [2 for i in range(9)]
            distribution.append(4)
            num = np.random.choice(np.array(distribution))
            # fills the cell with 2 or 4
            board[rowtofill][coltofill] = num
            return board
        else:
            # case when no empty cells
            return
    
    def __mergeCells(self,slice_to_merge,action):
        # first argument is a row/col as a 1d array,
        # second argument can be "left","right","up" or "down"
        # effect of "left" and "up" is the same, "right" and "down" also
        # finds cells to merge and returns the row/col as an array
        score_for_merge = 0
        if action == "r" or action == "d":
            slice_to_merge = slice_to_merge[::-1]

        if not np.all(slice_to_merge):
            # if there are zeros, shifts all the zeros to the right
            nonzero_elements = []
            for i in range(self.size):
                if slice_to_merge[i] != 0:
                    nonzero_elements.append(slice_to_merge[i])
            zeros = self.size - len(nonzero_elements)
            for _ in range(zeros):
                nonzero_elements.append(0)
            slice_to_merge = np.array(nonzero_elements)

        # find adjacent cells that are the same and merge
        for i in range(1, self.size):
            if slice_to_merge[i] == slice_to_merge[i-1] and slice_to_merge[i] != 0:
                slice_to_merge[i-1] *= 2
                slice_to_merge[i] = 0
                score_for_merge += slice_to_merge[i-1]

        # shift all the zeros to the right again
        if not np.all(slice_to_merge):
            nonzero_elements = []
            for i in range(self.size):
                if slice_to_merge[i] != 0:
                    nonzero_elements.append(slice_to_merge[i])
            zeros = self.size - len(nonzero_elements)
            for _ in range(zeros):
                nonzero_elements.append(0)
            slice_to_merge = np.array(nonzero_elements)
        if action == "r" or action == "d":
            return slice_to_merge[::-1], score_for_merge
        else:
            return slice_to_merge, score_for_merge

    def __gameOver(self):
        # checks if there are any possible moves left
        if np.all(self.board):
            # check that there are no empty cells
            can_merge = False
            
            # check if can merge with cell on the right
            for row in range(self.size):
                for col in range(self.size-1):
                    if self.board[row][col] == self.board[row][col+1]:
                        can_merge = True
            #check if can merge with cell below
            for row in range(self.size-1):
                for col in range(self.size):
                    if self.board[row][col] == self.board[row+1][col]:
                        can_merge = True
        # if there are empty cells, return gameover = False
        else:
            return False
        
        if can_merge == True:
            return False
        else:
            return True