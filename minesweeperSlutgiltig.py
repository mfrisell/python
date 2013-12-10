#########################################
###    Marcus Frisell    2013-12-10    ###
#########################################

import random, time, math
from tkinter import *

class Minesweeper():
    """ Konstruktor, bestämmer variabler och kör igång metoderna för att skapa spelmatrisen"""
    def __init__(self, gridSize, mineCount): 
        self.root = Tk() 
        self.root.title("Minröj") 
        self.root.geometry("+800+200") 
        self.frame = Frame(self.root) 
        self.frame.pack(side=TOP, padx=10, pady=10)
        self.frameHead = Frame(self.root)
        self.frameHead.pack(side=BOTTOM, pady=10) 
        self.modeButton = Button(self.frameHead, command=lambda: self.clickMode(), text="Skjut") #växla mellan skjut/flagga
        self.modeButton.pack(side=LEFT, padx=50)
        self.exitButton = Button(self.frameHead, command=lambda: self.exitMinesweeper(), text="Avsluta") #knapp - avslutar spelet
        self.exitButton.pack(side=RIGHT)
        self.restartButton = Button(self.frameHead, command=lambda: self.restartMinesweeper(), text="Starta Om") #knapp - startar om spelet
        self.restartButton.pack(side=RIGHT)
        self.flag = 0 #0 = skjuta är valt, 1 = flagga är valt
        self.name = "" #namn matas in av användaren vid vinst
        self.gridSize = gridSize
        self.mineCount = mineCount
        self.flagCount = 0 #antal utplacerade flaggor
        self.mineLeft = self.mineCount #antal minor kvar att träffa
        self.board = self.gameBoard(self.gridSize, self.root, self.frame)
        self.mineRandList = self.randCells(self.board, self.gridSize, self.mineCount) 
        self.insertCells(self.board, self.mineRandList) 
        self.checkCells(self.board) 
        self.start = 0 #0 = timer är inte startad, 1 = timern är startad
        self.timeCount = 0 #tiden som gått tills spelaren vunnit
        self.score = 0 #spelaren poäng
        
    """ Skapar spelmatrisen, där vi lägger alla min-objekt.
        Invariabler är storleken på spelplanen samt root-fönstret och hållaren för spelbrädet. """
    def gameBoard(self, gridSize, root, frame):
        board = []
        for i in range(1,gridSize+1):
            col = []
            for j in range(1,gridSize+1):       
                col.append(Cell(self, 0, 0, 0, j-1, i-1, 0, root, frame))
            board.append(col)
        return board 

    """ Väljer ut random koordinater från objekt ur spelmatrisen
        Invariabler är spelmatrisen, spelplansstorlek, och antal minor som ska skapas. """
    def randCells(self, board, gridSize, mineCount):
        mineList = []
        mineRandList = []
        for i in board:
            for j in i:
                mineList.append((j.cordX, j.cordY)) #koordinater från alla skapade objekt läggs till i listan mineList
        for i in range(int(mineCount)): 
            mineListCheck = mineList.pop(mineList.index(random.choice(mineList))) #utvalda värden tas bort från mineList så de inte väljs igen,
            mineRandList.append(mineListCheck)                                      #och läggs till i listan över valda värden
        return mineRandList

    """ De objekt med koordinater som valts ut i randCells blir uppdaterade till bomber.
        Invariabler är spelmatrisen och vår lista med random koordinater från randCells. """
    def insertCells(self, board, mineRandList): 
        for i in board: #går igenom spelmatrisen, och hämtar koordinaterna för varje objekt
            for k in i:
                mineCords = (k.cordX, k.cordY)
                if mineCords in mineRandList: 
                    k.mineStatus = 1
                    
    """ Grannarna kollas efter bomber, för varje hittad bomb uppdateras min-objektet i spelmatrisen
        och säger hur många bomber som finns runt omkring.
        Invariabel är spelmatrisen. """
    def checkCells(self, board): 
        for i in board:
            for k in i:
                moves = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)] #koordinater för grannceller
                for j in moves: 
                    try:
                        cordNewX = k.cordX + j[0] 
                        cordNewY = k.cordY + j[1]
                        if cordNewX > -1 and cordNewY > -1: #ifall de nya koordinaterna finns i spelmatrisen
                            k.minesAround += board[cordNewY][cordNewX].mineStatus #är den kollade cellen en bomb så ökar vi antalet omkringliggande bomber med 1
                    except IndexError:                                              
                        pass

    """ Klockan startar"""                   
    def startTimer(self):
        if(self.start==0): #Körs bara då self.start = 0, vilket den bara kommer vara första gången spelaren klickar
           self.timer = time.time()
           self.start=1

    """ När ett klick på en knapp i spelplanen sker så kollas det ifall man valt att flagga eller skjuta,
        sen kollar metoden om den klickade rutan har närliggande bomber eller om man klickat på en bomb.
        Invariabler är koordinaterna för den klickade rutan. """                    
    def click(self, x, y): 
        self.startTimer() 
        if(self.flag == 0): 
            if(self.board[y][x].flagStatus == 1):
                self.flagCount -=1
            if(self.board[y][x].mineStatus == 0): 
                if(self.board[y][x].minesAround != 0):         
                    self.board[y][x].button["text"] = self.board[y][x].minesAround
                    self.board[y][x].clickStatus = 1
                else:
                   self.getNeigh(x, y)
            else: #spelaren klickade på en bomb
                self.gameLoss()
        else: #spelaren har valt att flagga
            if(self.board[y][x].clickStatus == 0): 
                if(self.board[y][x].flagStatus == 0):             
                    self.board[y][x].flagStatus = 1 
                    self.flagCount +=1
                    self.board[y][x].button["text"] = "F"
                    if(self.board[y][x].mineStatus == 1):
                        self.mineLeft -= 1
                        if(self.mineLeft == 0 and self.flagCount <= self.mineCount): #finns det inga minor kvar och antalet utplacerade
                            self.gameWin()                                             #flaggor inte är fler än antalet minor som finns
                else: #avflagga ruta                                                   #så vinner man
                    self.board[y][x].flagStatus = 0
                    self.flagCount -=1
                    self.board[y][x].button["text"] = ""
                    if(self.board[y][x].mineStatus == 1):
                        self.mineLeft += 1

    """ Körs när en ruta som inte har några närliggande bomber(0) klickats.
        Metoden går igenom närliggande celler, och lägger till hittade (0),
        samt visar värdet på tittade celler för spelaren. Metoden körs tills det inte finns fler (0) i närheten.
        Invariabler är koordinaterna för den klickade rutan. """ 
    def getNeigh(self, x, y):
        moves = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)] #koordinater för grannceller
        zeroList = [(x, y)] #lista med koordinater för celler vars värde är 0 som ska gås igenom
        while(zeroList): 
            for j in moves:
                try:
                    cordNewX = zeroList[0][0] + j[0]
                    cordNewY = zeroList[0][1] + j[1]
                    if (cordNewX > -1 and cordNewY > -1) and (cordNewX < self.gridSize and cordNewY < self.gridSize):#finns koordinater inom spelmatrisen
                        if(self.board[cordNewY][cordNewX].clickStatus == 0):                                        
                            if(self.board[cordNewY][cordNewX].minesAround != 0):
                                self.board[cordNewY][cordNewX].button["text"] = self.board[cordNewY][cordNewX].minesAround
                                self.board[cordNewY][cordNewX].clickStatus = 1
                            else:
                                if(self.board[cordNewY][cordNewX].flagStatus == 0):
                                    zeroList.append((cordNewX, cordNewY)) #lägg till koordinaterna för cellen i zeroList
                                    self.board[cordNewY][cordNewX].button["state"] = DISABLED
                                    self.board[cordNewY][cordNewX].clickStatus = 1                    
                except IndexError:
                    pass               
            if(self.board[y][x].flagStatus == 0):
                self.board[y][x].clickStatus = 1
                zeroList.pop(0)
                self.board[y][x].button["state"] = DISABLED

    """ Spelaren växlar mellan att Skjuta eller Flagga. """ 
    def clickMode(self):
        if(self.flag == 0): #är skjuta valt
            self.flag = 1 
            self.modeButton["text"] = "Flagga"
        else: #är flagga valt
            self.flag = 0
            self.modeButton["text"] = "Skjut"
            
    """ Spelaren har klickat på en bomb. Hela spelplanen visas. Minesweeper Over. """ 
    def gameLoss(self):
        for i in self.board:
            for k in i:
                if(k.mineStatus == 1):
                    k.button["text"] = "#"
                else:
                    if(k.minesAround == 0):
                        k.button["text"] = ""
                    else:
                        k.button["text"] = k.minesAround
        self.lossPop = Tk()
        self.lossPop.title("Du dog")
        self.lossPop.geometry("+310+250")
        self.lossText = Label(self.lossPop, text="Du dog.").grid(column=1,row=1, pady=20, padx=30)
        self.lossExit = Button(self.lossPop, text="Avsluta", command=lambda: self.gameLossKill()).grid(column=1, row=2,pady=20, padx=30)

    """ Dödar lossPop och avslutar programmet. """
    def gameLossKill(self):
        self.lossPop.destroy()
        self.exitMinesweeper()

    """ Spelaren har hittat alla minor. Timern slutar räkna och poängen räknas ut.
        Popup som manar användaren att ange namn visas.""" 
    def gameWin(self):
        self.root.destroy()
        self.popup = Tk() # Skapar nytt fönster på högsta nivån.
        self.popup.title("Grattis du dog inte!")
        self.popup.geometry("+310+250")
        winText = Label(self.popup, text="Mata in ditt namn.").grid(column=1,row=1)
        self.nameGet = StringVar()
        winName = Entry(self.popup, textvariable=self.nameGet).grid(column=1,row=2, padx=20)
        winOk = Button(self.popup, text="OK", command=lambda: self.enterName(self.popup)).grid(column=1, row=3)
        self.timeCount = math.floor(time.time() - self.timer) #timer, vars värde kollas när gameWin körs
        matrix = self.gridSize*self.gridSize #matris, används i uträkningen för poäng
        minePercent = self.mineCount/matrix #räknar ut hur många procent av spelplanen som var minor
        self.score = math.floor((minePercent/(self.timeCount/matrix))*100) #uträkning av poäng

    """ När spelaren klickat OK så kommer popup:en stängas ned, namnet hämtas och metoder för highscore anropas. """
    def enterName(self, popup):
        self.popup.destroy()
        self.name = self.nameGet.get()
        self.readFile()
        self.writeFile()
        self.showHighscores()
        
    """ Highscorefilen läses in. Nuvarande spelare läggs till och poängen sorteras i fallande ordning. """ 
    def readFile(self):
        hsList = []
        text = open("highscores.txt", "r") #öppna highscore-fil
        lines = text.readlines() #läs in varje rad
        text.close()
        for i in lines:
            i = i.strip('\n').replace('{','').split(" | ") #gå igenom varje rad, dela den vid strecket och ta bort \n från strängen
            hsList.append((int(i[0]), i[1]))
        hsList.append((self.score, self.name)) #lägg till nuvarande spelares namn och poäng        
        self.sortedHs = sorted(hsList, key=lambda a: int(a[0]), reverse=True) #sortera listan efter poäng i fallande ordning

    """ Highscorefilen uppdateras med den nya spelaren. """ 
    def writeFile(self):
        updatedHs = open("highscores.txt", "w+") #öppna highscore-filen
        [updatedHs.write(str(int(i[0]))+" | "+i[1]+"\n") for i in self.sortedHs] #skriv in den nya sorterade listan (sortedHs) i filen

    """ De tio bästa spelarna i Highscore-listan skrivs ut. """ 
    def showHighscores(self):
        self.hsPop = Tk() # Skapar nytt fönster
        self.hsPop.title("Highscorelista")
        self.hsPop.geometry("+310+250")
        for i in range(10):
            try:
                hsNameString = str(i+1) + ".", self.sortedHs[i][1], str(self.sortedHs[i][0])+ "p"
                hsName = Label(self.hsPop, text=hsNameString).grid(row=i, padx=20, pady=5)
            except IndexError:
                pass

    """ Spelaren har valt att avsluta spelet. Döda root-fönstret. """ 
    def exitMinesweeper(self):
        self.root.destroy()
        
    """ Spelaren har valt att starta om spelet. Döda root-fönstret och initiera ett nytt spel. """ 
    def restartMinesweeper(self):
        self.root.destroy()
        gameInfo()
        
    """ Konstruktor, skapar objekten som innehåller all information om minorna. Knapparna i spelmatrisen skapas här.
        Invariabler är: ifall objektet är en mina, ifall objektet blivit kollat, antal närliggande bomber, koordinater
        ifall objektet blivit flaggat samt root-fönstret och hållaren för spelmatrisen. """
class Cell(Minesweeper):
    def __init__(self, parent, mineStatus, clickStatus, minesAround, cordX, cordY, flagStatus, root, frame):
        self.mineStatus = mineStatus #1 ifall objektet är en mina, 0 annars
        self.clickStatus = clickStatus #har objektet blivit kollat
        self.minesAround = minesAround #antal omkringliggande celler med mineStatus 1
        self.cordX = cordX #koordinatX för objektet
        self.cordY = cordY #koordinatY för objektet
        self.flagStatus = flagStatus #är objektet flaggad
        self.button = Button( #knapp som läggs i spelmatrisen
            frame,
            command=lambda: Minesweeper.click(parent, self.cordX, self.cordY), text="") 
        self.button.config(width="1",height="1")
        self.button.grid(column=self.cordX, row=self.cordY) #koordinater för knapparna så de lägger sig i en matris i vår frame i root-fönstret

class MineSweeperObject():
    def __init__(self, clickObject):
        self.clickObject = clickObject
        
""" Funktionen körs när användaren valt svårighetsnivå. Startar Spelet  """
def gameMode(optPop, gridSize, mineCount):
    Minesweeper(gridSize, mineCount)
    optPop.destroy()

""" Kollar ifall de inmatade värdena uppfyller kraven för att skapa spelplan. """
def gameModeCheck(optPop, gridSize, mineCount):
    if(gridSize.isdigit() and mineCount.isdigit()):
        if(((int(mineCount)/(int(gridSize)*int(gridSize)))*100) > 9 and int(gridSize)>4):
            gameMode(optPop, int(gridSize), int(mineCount))
        else:
            gameError()
    else:
        gameError()
        
""" Vid felinmatning, ge felmeddelande. """
def gameError():
    errorPop = Tk()
    errorPop.title("Fel värden inmatade")
    errorPop.geometry("+310+250")
    errorMessage = Label(errorPop, text="Du måste ange korrekta värden. Minst 10% måste vara minor").grid(pady=20, padx=20)

""" Funktion som manar användaren att uppge svårighetsnivå, eller mata in egna värden på spelplan och mintantal.  """
def gameOptions(infoPop):
    infoPop.destroy()
    optPop = Tk()
    optPop.title("Svårighetsgrad")
    optPop.geometry("+310+250")
    optEasy = Button(optPop, text="Lätt", command=lambda: gameMode(optPop, 10,10)).grid(column=1, row=1, pady=20)
    optMedium = Button(optPop, text="Mellan", command=lambda: gameMode(optPop, 15,23)).grid(column=2, row=1, pady=20)
    optHard = Button(optPop, text="Svår", command=lambda: gameMode(optPop, 20,40)).grid(column=3, row=1, pady=20)
    optText = Label(optPop, text="Eller välj egna värden").grid(column=2, row=2)
    optGridSize = Label(optPop, text="Spelplansstorlek (en led)").grid(column=1, row=3)
    optCellCount = Label(optPop, text="Minantal (minst 10%)").grid(column=3, row=3)
    optGridSize = StringVar()
    optGridEntry = Entry(optPop, textvariable=optGridSize).grid(column=1, row=4, padx=20, pady=20)
    optCellCount = StringVar()
    optCellEntry = Entry(optPop, textvariable=optCellCount).grid(column=3, row=4, padx=20, pady=20)
    optOwn = Button(optPop, text="OK", command=lambda: gameModeCheck(optPop, optGridSize.get(),optCellCount.get())).grid(column=2, row=4, pady=20)

""" Visar information innan spelstart """
def gameInfo():
    infoPop = Tk()
    infoPop.title("Information")
    infoText = Label(infoPop, text="Minröj\nDu kan välja svårighetsgrad, lätt, mellan eller svår.\nDu kan också mata in egna värden, vill du ha en 10x10 matris, skriver du 10.\nMinst 10% av spelplanen måste vara minor.\nFör att växla mellan att skjuta eller flagga minor klickar du på knappen under spelplanen.").grid(column=1,row=1, pady=20, padx=20)
    infoOk = Button(infoPop, text="OK", command=lambda: gameOptions(infoPop)).grid(column=1, row=2, pady=20, padx=20)

""" Startar programmet """
gameInfo()


    

