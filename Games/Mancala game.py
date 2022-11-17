class mancala:
    def __init__(self):
        self.turn = 0
        self.playing = True
        self.gameBoard = [[4,4,4,4,4,4,0],
                          [4,4,4,4,4,4,0]]
        
    def displayGame(self):
        print()
        print("        Player 1")
        print("######################")
        print("#",end="  ")
        for i in range(6):
            print(self.gameBoard[0][i],end="  ")
        print("#")
        print("#   {}".format(self.gameBoard[1][6]),end = "           {}    #".format(self.gameBoard[0][6]))
        print()
        print("#",end="  ")
        for i in range(6-1,-1,-1):
            print(self.gameBoard[1][i],end="  ")
        print("#")
        print("######################")
        print("        Player 2")
        print()

    def checkPockets(self):
        for a in range(2):
            tempBool = False
            for i in range(6):
                if self.gameBoard[a][i] > 0:
                    tempBool = True
            if not tempBool:
                self.playing = False

    def moveStones(self,pocket):
        side = self.turn
        if side == 0:
            notSide = 1
        else:
            notSide = 0
        tempSide = side
        moves = self.gameBoard[side][pocket]
        self.gameBoard[side][pocket] = 0
        for i in range(moves):
            if tempSide == self.turn:
                if pocket < 6:
                    pocket += 1
                else:
                    pocket = 0
                    tempSide = notSide
            else:
                if pocket < 5:
                    pocket += 1
                else:
                    pocket = 0
                    tempSide = side
            self.gameBoard[tempSide][pocket] += 1
            
        if tempSide == self.turn:
            if pocket == 6:
                print("Go again!")
                if self.turn == 0:
                    self.turn = 1
                else:
                    self.turn = 0
            elif self.gameBoard[side][pocket] == 1 and self.gameBoard[notSide][5 - pocket] > 0:
                print("Nice steal!")
                self.gameBoard[side][pocket] += self.gameBoard[notSide][5 - pocket]
                self.gameBoard[notSide][5 - pocket] = 0
        

    def playerMove(self):
        choice = 0
        while choice < 1 or choice > 6:
            try:
                if self.turn == 0:
                    print("Player 1")
                    choice = int(input("Please select a pocket with stones to empty (1-6, left to right, top row) : "))
                else:
                    print("Player 2")
                    choice = int(input("Please select a pocket with stones to empty (1-6, right to left, bottom row) : "))
            except:
                choice = 0
            if choice != 0:
                if self.gameBoard[self.turn][choice-1] == 0:
                    choice = 0
        self.moveStones(choice-1)

    def findWinner(self):
        for a in range(2):
            for i in range(6):
                self.gameBoard[a][6] += self.gameBoard[a][i]
                self.gameBoard[a][i] = 0
        print("Final board")
        self.displayGame()
        if self.gameBoard[0][6] > self.gameBoard[1][6]:
            print("Player 1 wins!")
        elif self.gameBoard[1][6] > self.gameBoard[0][6]:
            print("Player 2 wins!")
        else:
            print("It's a draw!")
        
    def gameLoop(self):
        print("""Player 1's pockets are the top six and their mancala is the right middle pocket.
Player 2's pockets are the bottom six and their mancala is the left middle pocket.
The game will go around the board in a clockwise motion.""")
        self.displayGame()
        while self.playing:
            self.playerMove()
            self.displayGame()
            if self.turn == 0:
                self.turn = 1
            else:
                self.turn = 0
            self.checkPockets()
        self.findWinner()

if __name__ == '__main__':
    newGame = mancala()
    newGame.gameLoop()
