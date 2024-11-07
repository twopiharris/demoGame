import pygame, simpleGE, random

"""demo.py"""

class Player(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.colorRect("blue", (50, 50))
        self.position = (320, 400)
        
    def process(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.x -= 5
        if self.isKeyPressed(pygame.K_RIGHT):
            self.x += 5
            
class Money(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.colorRect("darkgreen", (50, 25))
        
        self.reset()
        
    def reset(self):
        self.x = random.randint(0, self.screenWidth)
        self.y = 0
        self.dy = random.randint(3, 8)
        
    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()            

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.background.fill("papayawhip")
        self.player = Player(self)
        self.targets = []
        for i in range(10):
            self.targets.append(Money(self))

        self.score = 0
        self.lblScore = simpleGE.Label()
        self.lblScore.center = (100, 50)
        self.lblScore.text = f"Cash: $0"
        
        self.timer = simpleGE.Timer()
        self.lblTime = simpleGE.Label()
        self.lblTime.center = (400, 50)
        self.lblTime.text = f"Time Elapsed: "

        self.sprites = [self.player,
                        self.targets,
                        self.lblScore,
                        self.lblTime]
        
    def process(self):
        
        #manage collisions
        for money in self.targets:
            if self.player.collidesWith(money):
                money.reset()
                self.score += 20000
                self.lblScore.text = f"Cash: ${self.score}"
                if self.score > 1000000:
                    print (self.timer.getElapsedTime())
                    self.stop()

        #manage time
        self.time = self.timer.getElapsedTime()
        timeString = f"Time: {self.time:.2f} sec."
        self.lblTime.text = timeString

class Instructions(simpleGE.Scene):
    def __init__(self, lastTime):
        super().__init__()
        self.background.fill("papayawhip")
        self.nextAction = "quit"
        self.lblDirections = simpleGE.MultiLabel()
        self.lblDirections.textLines = [
            "You are the box at the bottom of the screen",
            "Move left and right with the arrow keys",
            "Catch the money as it falls.",
            "How quickly can you get to a million dollars?",
            f"(Last time: {lastTime:.2f} seconds)",
            "",
            "escape to quit",
            "Click to start."]
        self.lblDirections.center = (320, 240)
        self.lblDirections.size = (500, 300)
        
        self.sprites = [self.lblDirections]
            
    def process(self):
        if self.lblDirections.clicked:
            self.nextAction = "play"
            self.stop()
            
        if self.isKeyPressed(pygame.K_ESCAPE):
            self.nextAction = "quit"
            self.stop()

def main():
    keepGoing = True
    lastTime = 0.0
    while keepGoing:
        instructions = Instructions(lastTime)
        instructions.start()
        if instructions.nextAction == "play":        
            game = Game()
            game.start()
            lastTime = game.time
        else:
            keepGoing = False
           
           
if __name__ == "__main__":
    main()
