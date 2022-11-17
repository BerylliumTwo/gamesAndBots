import pygame, random

pygame.init()

class newBot:
    def __init__(self, firstGen = True, BallUpWeight = 0, BallDownWeight = 0, PaddleUpWeight = 0, PaddleDownWeight = 0):
        self.paddleRect = pygame.Rect((50,220),(10,75))
        if firstGen:
            self.BallPosWeightUp = random.uniform(-1,1)
            self.BallPosWeightDown = random.uniform(-1,1)
            self.PaddlePosWeightUp = random.uniform(-1,1)
            self.PaddlePosWeightDown = random.uniform(-1,1)
        else:
            self.BallPosWeightUp = BallUpWeight + random.uniform(-.1,.1)
            self.BallPosWeightDown = BallDownWeight + random.uniform(-.1,.1)
            self.PaddlePosWeightUp = PaddleUpWeight + random.uniform(-.1,.1)
            self.PaddlePosWeightDown = PaddleDownWeight + random.uniform(-.1,.1)
    
    def move(self, dist):
        if self.paddleRect.centery > 50 and dist < 0:
            self.paddleRect.centery += dist
        if self.paddleRect.centery < 450 and dist > 0:
            self.paddleRect.centery += dist

    def makeDecision(self, ballPos):
        optionUp = 0
        optionDown = 0

        optionUp += (self.BallPosWeightUp*ballPos) + (self.PaddlePosWeightUp*self.paddleRect.centery)
        optionDown += (self.BallPosWeightDown*ballPos) + (self.PaddlePosWeightDown*self.paddleRect.centery)        

        if optionUp > optionDown:
            self.move(-5)
        else:
            self.move(5)
        
    def getPara(self):
        return self.BallPosWeightUp, self.BallPosWeightDown, self.PaddlePosWeightUp, self.PaddlePosWeightDown

class newSim:
    def __init__(self):
        size = (700,500)
        self.scr = pygame.display.set_mode(size)
        pygame.display.set_caption("Pong Bot")
        self.playing = True
        self.hideScr = False
        self.playerCount = 500000
        self.playerList = [newBot() for i in range(self.playerCount)]
        self.ballRect = pygame.Rect((345,245),(10,10))
        self.ballX = -4
        self.ballY = 1
        self.genCount = 1

    def mainLoop(self):
        clock = pygame.time.Clock()
        while self.playing:
            self.moveBall()
            if not self.hideScr:
                self.drawScreen()
            for each in self.playerList:
                each.makeDecision(self.ballRect.centery)
            self.checkEvents()
            clock.tick(240)
        pygame.quit()

    def moveBall(self):
        self.ballRect.centerx += self.ballX
        self.ballRect.centery += self.ballY
        if self.ballRect.centerx > 650:
            self.ballX *= -1
        elif self.ballRect.centerx < 20:
            self.playerList = [newBot(False,*self.playerList[0].getPara()) for i in range(self.playerCount-1)]
            self.playerList.append(newBot())
            self.genCount += 1
            self.ballRect.centerx = 345
            
        if self.ballRect.centery > 480:
            self.ballRect.centery = 480
            self.ballY *= -1
        elif self.ballRect.centery < 20:
            self.ballRect.centery = 20
            self.ballY *= -1

    def drawScreen(self):
        white = (255,255,255)
        black = (0,0,0)
        
        self.scr.fill(black)
        pygame.draw.rect(self.scr,white,self.ballRect)
        for each in self.playerList:
            pygame.draw.rect(self.scr,white,each.paddleRect)
        pygame.draw.line(self.scr,white,(349,0),(349,500),5)

        pygame.display.flip()
        

    def checkEvents(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(self.genCount)
                self.playing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.hideScr = not self.hideScr
                    print(len(self.playerList))

        collide = False

        for each in self.playerList:
            if not collide:
                if each.paddleRect.colliderect(self.ballRect):
                    self.ballX *= -1
                    self.ballY = random.choice([i for i in range(-4,4) if i != 0])
                    self.ballRect.centerx += 5
                    for i in range(len(self.playerList)-1,-1,-1):
                        if self.playerList[i].paddleRect.centery < self.ballRect.centery - 50 or self.playerList[i].paddleRect.centery > self.ballRect.centery + 50:
                            self.playerList.pop(i)
                    collide = True
                        
if __name__ == "__main__":
    Sim = newSim()
    Sim.mainLoop()
