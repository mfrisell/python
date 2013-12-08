import random
from tkinter import *

class Game():
    def __init__(self, root):
        self.root = root
        self.gridSize = int(input("Spelplansstorlek: "))
        self.board = self.gameBoard(self.gridSize, self.root)
        self.mineRandList = self.randMines(self.board, self.gridSize)
        self.insertMines(self.board, self.mineRandList)
        self.checkMines(self.board)
        self.showBoard(self.board)

    def gameBoard(self, gridSize, root):
        board = []
        for i in range(1,gridSize+1):
            col = []
            for j in range(1,gridSize+1):       
                col.append(Mine(0, 0, 0, j-1, i-1, 0, root))
            board.append(col)
        return board

    def randMines(self, board, gridSize):
        mineList = []
        mineRandList = []
        for i in board:
            for j in i:
                mineList.append((j.cordX, j.cordY))
        for i in range(int((gridSize*gridSize)/8)):
            mineListCheck = mineList.pop(mineList.index(random.choice(mineList)))
            mineRandList.append(mineListCheck)
        return mineRandList

    def insertMines(self, board, mineRandList):
        for i in board:
            for k in i:
                mineCords = (k.cordX, k.cordY)
                if mineCords in mineRandList:
                    k.mineStatus = 1

    def checkMines(self, board):
        for i in board:
            for k in i:
                moves = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
                for j in moves:
                    try:
                        cordNewX = k.cordX + j[0]
                        cordNewY = k.cordY + j[1]

                        if cordNewX > -1 and cordNewY > -1:
                            k.minesAround += board[cordNewY][cordNewX].mineStatus

                    except IndexError:
                        pass

    def showBoard(self, board):
        row = []
        for i in board:
            col = []
            for k in i:
                if(k.mineStatus == 1):
                    col.append("#")
                else:
                    col.append((str(k.minesAround)))
            row.append(col)
        for i in row:
            print(i)
                    
                        
    def click(self, x, y):
        if(self.board[y][x].mineStatus == 0):
            
            if(self.board[y][x].minesAround != 0):            
                self.board[y][x].button["text"] = self.board[y][x].minesAround
            else:
               self.neighbours(x, y) #Visa omkringliggande      

        else: #Game Over
            for i in self.board:
                for k in i:
                    if(k.mineStatus == 1):
                        k.button["text"] = "#"
                    else:
                        if(k.minesAround == 0):
                            k.button["text"] = ""
                        else:
                            k.button["text"] = k.minesAround
                            
    def neighbours(self, x, y):
        moves = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        zeroList = [(x, y)]
        zeroListChecked = []
        
        while len(zeroList) > 0:
            print(zeroList)
            x, y = zeroList.pop(0)
            zeroListChecked.append((x, y))
            for j in moves:
                    try:
                        cordNewX = x + j[0]
                        cordNewY = y + j[1]
                        if cordNewX > -1 and cordNewY > -1:
                            
                            if((self.board[cordNewY][cordNewX].minesAround == 0)):
                                zeroList.append((cordNewY, cordNewX))
                            
                            else:
                                self.board[cordNewY][cordNewX].button["text"] = self.board[cordNewY][cordNewX].minesAround
                                
                    except IndexError:
                        pass


class Mine():
    def __init__(self, mineStatus, clickStatus, minesAround, cordX, cordY, flagStatus, root):
        self.mineStatus = mineStatus
        self.clickStatus = clickStatus
        self.minesAround = minesAround
        self.cordX = cordX
        self.cordY = cordY
        self.flagStatus = flagStatus
        
        #Knappar
        self.root = root
        self.root.title("Minröj")
        self.root.geometry("+800+200")
        self.button = Button(
            command=lambda: Game.click(game, self.cordX, self.cordY)
            )
        self.button.config(width="1",height="1")
        self.button.grid(column=self.cordX, row=self.cordY)

root = Tk()
game = Game(root)            
                
#def main():
#    root = Tk()
#    game = Game(root)
#main()


    


