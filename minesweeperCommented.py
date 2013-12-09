#########################################
###    Marcus Frisell    2013-12-09    ###
#########################################

import random, time, math
from tkinter import *

class Game():
    """ Konstruktor, bestämmer variabler och kör igång metoderna för att skapa spelmatrisen"""
    def __init__(self): 
        self.root = Tk() #root-fönster
        self.root.title("Minröj")
        self.root.geometry("+800+200") #vart root-fönstret ska vara placerat på skärmen
        self.frame = Frame(self.root) #plats för spelplan
        self.frame.pack(side=TOP, padx=10, pady=10)
        self.frameHead = Frame(self.root) #plats för andra knappar
        self.frameHead.pack(side=BOTTOM, pady=10) 
        self.modeButton = Button(self.frameHead, command=lambda: self.clickMode(), text="Skjut") #växla mellan skjut/flagga
        self.modeButton.pack(side=LEFT, padx=50)
        self.exitButton = Button(self.frameHead, command=lambda: self.exitGame(), text="Avsluta") #knapp - avslutar spelet
        self.exitButton.pack(side=RIGHT)
        self.restartButton = Button(self.frameHead, command=lambda: self.restartGame(), text="Starta Om") #knapp - startar om spelet
        self.restartButton.pack(side=RIGHT)
        
        self.flag = 0 #0 = skjuta är valt, 1 = flagga är valt
        self.name = str(input("Namn: "))
        self.gridSize = int(input("Spelplansstorlek: "))
        self.mineCount = int(input("Antal minor: "))
        self.flagCount = 0 #antal utplacerade flaggor
        self.mineLeft = self.mineCount #antal minor kvar att träffa
        self.board = self.gameBoard(self.gridSize, self.root, self.frame) #anropar metod som skapar spelmatrisen
        self.mineRandList = self.randMines(self.board, self.gridSize, self.mineCount) #anropar metod som skapar random minor
        self.insertMines(self.board, self.mineRandList) #anropar metod som lägger in de skapade random minorna i spelmatrisen
        self.checkMines(self.board) #anropar metod som letar efter närliggande bomber
        self.start = 0 #0 = timer är inte startad, 1 = timern är startad
        self.timeCount = 0 #tiden som gått tills spelaren vunnit
        self.score = 0 #spelaren poäng
        
    """ Skapar spelmatrisen, där vi lägger alla min-objekt.
        Invariabler är storleken på spelplanen samt root-fönstret och hållaren för spelbrädet. """
    def gameBoard(self, gridSize, root, frame): #en lista med listor med objekt i skapas
        board = []
        for i in range(1,gridSize+1):
            col = []
            for j in range(1,gridSize+1):       
                col.append(Mine(0, 0, 0, j-1, i-1, 0, root, frame)) #objekt skapas och läggs i vår spelmatris (board)
            board.append(col)
        return board #board skickas tillbaka så den kan anropas från hela programmet

    """ Väljer ut random koordinater från objekt ur spelmatrisen
        Invariabler är spelmatrisen, spelplansstorlek, och antal minor som ska skapas. """
    def randMines(self, board, gridSize, mineCount): #Välj ut random nummer
        mineList = []
        mineRandList = []
        for i in board:
            for j in i:
                mineList.append((j.cordX, j.cordY)) #koordinater från alla skapade objekt läggs till i listan mineList
        for i in range(int(mineCount)): #en loop som kör så många gånger som det ska skapas minor
            mineListCheck = mineList.pop(mineList.index(random.choice(mineList))) #utvalda värden tas bort från mineList så de inte väljs igen,
            mineRandList.append(mineListCheck)                                      #och läggs till i listan över valda värden
        return mineRandList #returnera listan med utvalda objekt

    """ De objekt med koordinater som valts ut i randMines blir uppdaterade till bomber.
        Invariabler är spelmatrisen och vår lista med random koordinater från randMines. """
    def insertMines(self, board, mineRandList): #listan med utvalda objekt hämtas in
        for i in board: #går igenom spelmatrisen, och hämtar koordinaterna för varje objekt
            for k in i:
                mineCords = (k.cordX, k.cordY)
                if mineCords in mineRandList: #finns koordinaterna som hämtats även i listan med utvalda objekt så skapas en bomb
                    k.mineStatus = 1
                    
    """ Grannarna kollas efter bomber, för varje hittad bomb uppdateras min-objektet i spelmatrisen
        och säger hur många bomber som finns runt omkring.
        Invariabel är spelmatrisen. """
    def checkMines(self, board): #Kolla omkringliggande efter minor
        for i in board:
            for k in i:
                moves = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)] #alla omkringliggande celler
                for j in moves: #vi kollar grannar efter bomber
                    try:
                        cordNewX = k.cordX + j[0] #ursprungskoordinater + koordinater för att få grannarnas koordinater
                        cordNewY = k.cordY + j[1]
                        if cordNewX > -1 and cordNewY > -1: #ifall de nya koordinaterna finns i spelmatrisen
                            k.minesAround += board[cordNewY][cordNewX].mineStatus #är den kollade cellen en bomb så ökar vi antalet
                    except IndexError:                                              #omkringliggande bomber med 1
                        pass

    """ Klockan startar"""                   
    def startTimer(self):
        if(self.start==0): #Körs bara då self.start = 0, vilket den bara kommer vara första gången spelaren klickar
           self.timer = time.time()
           self.start=1

    """ När ett klick på en knapp i spelplanen sker så kollas det ifall man valt att flagga eller skjuta,
        sen kollar metoden om den klickade rutan har närliggande bomber eller om man klickat på en bomb.
        Invariabler är koordinaterna för den klickade rutan. """                    
    def click(self, x, y): #Ruta klickad
        self.startTimer() #metoden för att starta klockan anropas
        if(self.flag == 0): #ifall spelaren valt att skjuta och inte flagga
            if(self.board[y][x].flagStatus == 1):
                self.flagCount -=1 #skjuter spelaren en flagga så tas en flagga bort från antalet utplacerade flaggor
            if(self.board[y][x].mineStatus == 0): #har spelaren skjutit en cell som inte är en bomb
                if(self.board[y][x].minesAround != 0): #är värdet inte 0 så visa cellens värde         
                    self.board[y][x].button["text"] = self.board[y][x].minesAround
                    self.board[y][x].clickStatus = 1 #ändra cellens status till synlig
                else:
                   self.getNeigh(x, y) #cellens värde är 0, anropa metoden getNeigh
            else: #spelaren klickade på en bomb, anropa metoden gameLoss
                self.gameLoss()
        else: #spelaren har valt att flagga
            if(self.board[y][x].clickStatus == 0): #om en cell inte visats än kan den flaggas
                if(self.board[y][x].flagStatus == 0): #om en cell inte är en flagga             
                    self.board[y][x].flagStatus = 1 #flagga den
                    self.flagCount +=1
                    self.board[y][x].button["text"] = "F"
                    if(self.board[y][x].mineStatus == 1): #om spelaren flaggar en cell där det finns en mina
                        self.mineLeft -= 1 #minska antalet minor som finns kvar med 1
                        if(self.mineLeft == 0 and self.flagCount <= self.mineCount): #finns det inga minor kvar och antalet utplacerade
                            self.gameWin()                                              #flaggor inte är fler än antalet minor som finns
                else: #avflagga ruta                                                    #så vinner man
                    self.board[y][x].flagStatus = 0 #cellen är avflaggad
                    self.flagCount -=1 #minska antalet utplacerade flaggor med 1
                    self.board[y][x].button["text"] = "*" #visa en asterisk eftersom fältet är tomt
                    if(self.board[y][x].mineStatus == 1): #hade spelaren flaggat en mina så ökar antalet minor kvar med 1
                        self.mineLeft += 1

    """ Körs när en ruta som inte har några närliggande bomber(0) klickats.
        Metoden går igenom närliggande celler, och lägger till hittade (0),
        samt visar värdet på tittade celler för spelaren. Metoden körs tills det inte finns fler (0) i närheten.
        Invariabler är koordinaterna för den klickade rutan. """ 
    def getNeigh(self, x, y): #Visa omkringliggande
        moves = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)] #koordinater för grannceller
        zeroList = [(x, y)] #lista med koordinater för celler vars värde är 0
        while(zeroList): #så länge listan inte är tom så körs koden under
            for j in moves: #gå igenom granncellskoordinater
                try:
                    cordNewX = zeroList[0][0] + j[0] #ursprungskoordinater + granncellskoordinater
                    cordNewY = zeroList[0][1] + j[1]
                    if (cordNewX > -1 and cordNewY > -1) and (cordNewX < game.gridSize and cordNewY < game.gridSize):#finns koordinater inom
                        if(self.board[cordNewY][cordNewX].clickStatus == 0):                                           #spelmatrisen
                            if(self.board[cordNewY][cordNewX].minesAround != 0): #cellens värde är inte 0
                                self.board[cordNewY][cordNewX].button["text"] = self.board[cordNewY][cordNewX].minesAround #visa klickad cell
                                self.board[cordNewY][cordNewX].clickStatus = 1 #cellen har blivit kollad
                            else:
                                if(self.board[cordNewY][cordNewX].flagStatus == 0):#cellens värde är 0
                                    zeroList.append((cordNewX, cordNewY)) #lägg till koordinaterna för cellen i zeroList
                                    self.board[cordNewY][cordNewX].button["text"] = "" #ändra texten till "", cellen innehåller inget, den är
                                    self.board[cordNewY][cordNewX].clickStatus = 1     #oklickbar                     
                except IndexError:
                    pass               
            if(self.board[y][x].flagStatus == 0): #så länge cellen inte är flaggad
                self.board[y][x].clickStatus = 1 #cellen har blivit kollad
                zeroList.pop(0) #ta bort värdet ur zeroList
                self.board[y][x].button["text"] = "" #ändra texten till "", cellen innehåller inget, den är oklickbar

    """ Spelaren växlar mellan att Skjuta eller Flagga. """ 
    def clickMode(self): #Flagga eller skjut
        if(self.flag == 0): #är skjuta valt
            self.flag = 1 #ändra till flagga
            self.modeButton["text"] = "Flagga" #byt ut knapp-texten
        else: #är flagga valt
            self.flag = 0 #ändra till skjuta
            self.modeButton["text"] = "Skjut" #byt ut knapp-texten
            
    """ Spelaren har klickat på en bomb. Hela spelplanen visas. Game Over. """ 
    def gameLoss(self):
        for i in self.board: #gå igenom alla objekt i spelmatrisen
            for k in i:
                if(k.mineStatus == 1):
                    k.button["text"] = "#" #ifall objektet/cellen är en mina, visa det
                else:
                    if(k.minesAround == 0): #ifall objektets/cellens värde är 0, visa ""
                        k.button["text"] = ""
                    else:
                        k.button["text"] = k.minesAround #ifall objektet/cellen har ett värde över 0 och inte är en mina, visa värdet

    """ Spelaren har hittat alla minor. Timern slutar räkna och poängen räknas ut. Metoder för highscore anropas. """ 
    def gameWin(self):
        print("Grattis du vann")
        self.timeCount = math.floor(time.time() - self.timer) #timer, vars värde kollas när gameWin körs
        matrix = self.gridSize*self.gridSize #matris, används i uträkningen för poäng
        minePercent = self.mineCount/matrix #räknar ut hur många procent av spelplanen var minor
        self.score = math.floor((minePercent/(self.timeCount/matrix))*100) #uträkning av poäng
        self.readFile() #metod för att läsa in fil anropas      #(procent minor/(tiden det tog att vinna/antal celler)) multiplicerat med 100
        self.writeFile() #metod för att skriva till filen anropas
        self.showHighscores() #metod för att visa highscore anropas

    """ Highscorefilen läses in. Nuvarande spelare läggs till och poängen sorteras i fallande ordning. """ 
    def readFile(self): #Läs in fil
        hsList = []
        text = open("highscores.txt", "r") #öppna highscore-fil
        lines = text.readlines() #läs in varje rad
        text.close()
        for i in lines:
            i = i.strip('\n').split(" | ") #gå igenom varje rad, dela den vid strecket och ta bort \n från strängen
            hsList.append((int(i[0]), i[1])) #lägg till utlästa värden till en highscore-lista
        hsList.append((self.score, self.name)) #lägg till nuvarande spelares namn och poäng till listan         
        self.sortedHs = sorted(hsList, key=lambda a: int(a[0]), reverse=True) #sortera listan efter poäng i fallande ordning

    """ Highscorefilen uppdateras med den nya spelaren. """ 
    def writeFile(self): #Skriv in alla nya, sorterade värden i textfilen
        updatedHs = open("highscores.txt", "w+") #öppna highscore-filen
        [updatedHs.write(str(int(i[0]))+" | "+i[1]+"\n") for i in self.sortedHs] #skriv in den nya sorterade listan (sortedHs) i filen

    """ De tio bästa spelarna i Highscore-listan skrivs ut. """ 
    def showHighscores(self):
        for i in range(10):
            print(str(i+1) + ".", self.sortedHs[i][1], "- ", str(self.sortedHs[i][0]) + "p") #skriv ut de tio översta raden från highscore-filen

    """ Spelaren har valt att avsluta spelet. Döda root-fönstret. """ 
    def exitGame(self): #Avsluta spel
        self.root.destroy() #döda root-fönstret
        
    """ Spelaren har valt att starta om spelet. Döda root-fönstret och initiera ett nytt spel. """ 
    def restartGame(self): #Starta om spel
        self.root.destroy() #döda root-fönstret
        self.__init__() #initiera nytt spel
        
    """ Konstruktor, skapar objekten som innehåller all information om minorna. Knapparna i spelmatrisen skapas här.
        Invariabler är: ifall objektet är en mina, ifall objektet blivit kollat, antal närliggande bomber, koordinater
        ifall objektet blivit flaggat samt root-fönstret och hållaren för spelmatrisen. """
class Mine(): #Minobjekt
    def __init__(self, mineStatus, clickStatus, minesAround, cordX, cordY, flagStatus, root, frame):
        self.mineStatus = mineStatus #1 ifall objektet är en mina, 0 annars
        self.clickStatus = clickStatus #har objektet blivit kollat
        self.minesAround = minesAround #antal omkringliggande celler med mineStatus 1
        self.cordX = cordX #koordinatX för objektet
        self.cordY = cordY #koordinatY för objektet
        self.flagStatus = flagStatus #är objektet flaggad
        self.button = Button( #knapp som läggs i spelmatrisen
            frame,
            command=lambda: Game.click(game, self.cordX, self.cordY), text="*") #knappen anropar metoden click och skickar med koordinaterna
        self.button.config(width="1",height="1") #storlek på knapparna (gör ingen skillnad på mac, förutom bredd)
        self.button.grid(column=self.cordX, row=self.cordY) #koordinater för knapparna så de lägger sig i en matris i vår frame i root-fönstret

    """ Startar spelet """
game = Game() #Starta spel
