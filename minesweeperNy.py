import random
from tkinter import *

class Game():
    def __init__(self):

        self.root = Tk()
        self.root.title("Minröj")
        self.root.geometry("+800+200")
        self.frame = Frame(self.root)
        self.frame.pack(side=TOP, padx=10, pady=10)
        self.frameHead = Frame(self.root)
        self.frameHead.pack(side=BOTTOM, pady=10)
        self.modeButton = Button(self.frameHead, command=lambda: self.clickMode(), text="Skjut")
        self.modeButton.pack()

        self.flag = 0
        self.gridSize = int(input("Spelplansstorlek: "))
        self.mineCount = int(input("Antal minor: "))
        self.flagCount = 0
        self.mineLeft = self.mineCount
        self.board = self.gameBoard(self.gridSize, self.root, self.frame)
        self.mineRandList = self.randMines(self.board, self.gridSize, self.mineCount)
        self.insertMines(self.board, self.mineRandList)
        self.checkMines(self.board)

        #self.showBoard(self.board)

    def gameBoard(self, gridSize, root, frame):
        board = []
        for i in range(1,gridSize+1):
            col = []
            for j in range(1,gridSize+1):       
                col.append(Mine(0, 0, 0, j-1, i-1, 0, root, frame))
            board.append(col)
        return board

    def randMines(self, board, gridSize, mineCount):
        mineList = []
        mineRandList = []
        for i in board:
            for j in i:
                mineList.append((j.cordX, j.cordY))
        for i in range(int(mineCount)):
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

##    def showBoard(self, board):
##        row = []
##        for i in board:
##            col = []
##            for k in i:
##                if(k.mineStatus == 1):
##                    col.append("#")
##                else:
##                    col.append((str(k.minesAround)))
##            row.append(col)
##        for i in row:
##            print(i)
                    
                        
    def click(self, x, y):
        if(self.flag == 0):
        
            if(self.board[y][x].mineStatus == 0):
                
                if(self.board[y][x].minesAround != 0): #Visa ruta           
                    self.board[y][x].button["text"] = self.board[y][x].minesAround
                    self.board[y][x].clickStatus = 1
                else:
                   self.getNeigh(x, y) #Visa omkringliggande      

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
        else: #Flagga ruta
            if(self.board[y][x].clickStatus == 0):
            
                if(self.board[y][x].flagStatus == 0):               
                    self.board[y][x].flagStatus = 1
                    self.flagCount +=1
                    self.board[y][x].button["text"] = "F"
                    if(self.board[y][x].mineStatus == 1):
                        self.mineLeft -= 1
 #                       print("minor kvar: ", self.mineLeft)
 #                       print("placerade flaggor: ", self.flagCount)
                        if(self.mineLeft == 0 and self.flagCount <= self.mineCount):
                            print("Grattis du vann")
                else:
                    self.board[y][x].flagStatus = 0
                    self.flagCount -=1
                    self.board[y][x].button["text"] = ""
                    if(self.board[y][x].mineStatus == 1):
                        self.mineLeft += 1
            else:
                pass

        
    def getNeigh(self, x, y):
        moves = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        zeroList = [(x, y)]
        while(zeroList):
            for j in moves:
                try:
                    cordNewX = zeroList[0][0] + j[0]
                    cordNewY = zeroList[0][1] + j[1]

                    if (cordNewX > -1 and cordNewY > -1) and (cordNewX < game.gridSize and cordNewY < game.gridSize):
                        if(self.board[cordNewY][cordNewX].clickStatus == 0):

                            if(self.board[cordNewY][cordNewX].minesAround != 0):
                                self.board[cordNewY][cordNewX].button["text"] = self.board[cordNewY][cordNewX].minesAround
                                self.board[cordNewY][cordNewX].clickStatus = 1
                            else:
                                zeroList.append((cordNewX, cordNewY))
                                self.board[cordNewY][cordNewX].button["text"] = "0"
                                self.board[cordNewY][cordNewX].clickStatus = 1
                       
                except IndexError:
                    pass
                
            self.board[y][x].clickStatus = 1
            zeroList.pop(0)
            self.board[y][x].button["text"] = "0"
            
    def clickMode(self):
        if(self.flag == 0):
            self.flag = 1
            self.modeButton["text"] = "Flagga"
        else:
            self.flag = 0
            self.modeButton["text"] = "Skjut"

class Mine():
    def __init__(self, mineStatus, clickStatus, minesAround, cordX, cordY, flagStatus, root, frame):
        self.mineStatus = mineStatus
        self.clickStatus = clickStatus
        self.minesAround = minesAround
        self.cordX = cordX
        self.cordY = cordY
        self.flagStatus = flagStatus
        
        self.button = Button(
            frame,
            command=lambda: Game.click(game, self.cordX, self.cordY)
            )
        self.button.config(width="1",height="1")
        self.button.grid(column=self.cordX, row=self.cordY)

game = Game()
               
#def main():
#    root = Tk()
#    game = Game(root)
#main()


    


