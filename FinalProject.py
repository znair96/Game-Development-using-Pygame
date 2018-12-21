import pygame, random, sys
import time

pygame.init()

screen_width = 1200
screen_height = 600

white = (255,255,255)
black = (0,0,0)

canvas = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Maryo")

mainMenuImg = pygame.image.load("start.png")
mainMenuRect = mainMenuImg.get_rect()

cactusImg = pygame.image.load("cactus_bricks.png")
cactusRect = cactusImg.get_rect()
cactusRect.centerx = screen_width/2
cactusRect.centery = -100

fireImg = pygame.image.load("fire_bricks.png")
fireRect = fireImg.get_rect()
fireRect.centerx = screen_width/2
fireRect.centery = screen_height + 100

maryoImg = pygame.image.load("maryo.png")
maryoRect = maryoImg.get_rect()

dragonImg = pygame.image.load("dragon.png")
dragonRect = dragonImg.get_rect()

gameover = pygame.image.load("end.png")
gameoverRect = gameover.get_rect()

flameImg = pygame.image.load("fireball.png")
flameRect = flameImg.get_rect()

font = pygame.font.SysFont(None,25)

clock = pygame.time.Clock()

fps = 30

topScore = 0

smallfont = pygame.font.SysFont(None,25)
medfont = pygame.font.SysFont("comicsansms",50)
largefont = pygame.font.SysFont("comicsansms",80)


def terminate():
    pygame.quit()
    sys.exit()

def mainMenu():

    menu = True

    while menu:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                else:
                    menu = False

        mainMenuRect.centerx = screen_width/2
        mainMenuRect.centery = screen_height/2

        canvas.blit(mainMenuImg, mainMenuRect)
        pygame.display.update()
        clock.tick(5)

def displayText(msg,color,disp = 25,size="small"):
    #textSurf = font.render(msg,True,color)
    if size == "small":
        textSurf = smallfont.render(msg, True, color)
    if size == "medium":
        textSurf = medfont.render(msg, True, color)
    if size == "large":
        textSurf = largefont.render(msg, True, color)
        
    textRect = textSurf.get_rect()
    textRect.center = (screen_width/2), cactusRect.bottom + disp
    canvas.blit(textSurf,textRect)
    

#L1 = L2 = L3 = L4 = True

def checkLevel(score):
    
    #global L1, L2, L3, L4
    global cactusRect, fireRect, cactusImg, fireImg
    if score in range(0,250):# and L1:
        cactusRect.centery = -50
        fireRect.centery = screen_height + 50
        canvas.blit(cactusImg, cactusRect)
        canvas.blit(fireImg, fireRect)
        return 1
        
    elif score in range(250,500):# and L2:
        cactusRect.centery = 0
        fireRect.centery = screen_height
        canvas.blit(cactusImg, cactusRect)
        canvas.blit(fireImg, fireRect)
        return 2
        
    elif score in range(500,750):# and L3:
        cactusRect.centery = 50
        fireRect.centery = screen_height - 50
        canvas.blit(cactusImg, cactusRect)
        canvas.blit(fireImg, fireRect)
        return 3
    
    elif score > 750:# and L4:
        cactusRect.centery = 100
        fireRect.centery = screen_height - 100
        canvas.blit(cactusImg, cactusRect)
        canvas.blit(fireImg, fireRect)
        return 4


def gameOver():

    GameOver = True

    pygame.mixer.music.load("mario_dies.wav")
    pygame.mixer.music.play(1)
    while GameOver:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                else:
                    pygame.mixer.music.stop()
                    GameOver = False

        gameoverRect.centerx = screen_width/2
        gameoverRect.centery = screen_height/2

        canvas.blit(gameover, gameoverRect)
        pygame.display.update()
        clock.tick(5)

    gameLoop()


class Flames:

    global maryoRect, maryoImg
    
    flameSpeed = 13
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.img = flameImg
        self.imgRect = flameRect

    def render(self):
        self.imgRect.center = self.x , self.y
        canvas.blit(self.img, self.imgRect)

    def update(self):
        self.x -= Flames.flameSpeed
        
    def collision(self):
        if float(self.imgRect.left) <= float(maryoRect.right) and float(self.imgRect.right) >= float(maryoRect.left) and ((float(self.imgRect.top) >= float(maryoRect.top) and float(self.imgRect.top) <= float(maryoRect.bottom)) or (float(self.imgRect.bottom) >= float(maryoRect.top) and float(self.imgRect.bottom) <= float(maryoRect.bottom))):
            gameOver()

    @classmethod 
    def changeFlameSpeed(cls,x):
        Flames.flameSpeed = x

class Dragon:
    global cactusRect, fireRect
    velocity = 13
    up = True
    down = False

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.img = dragonImg
        self.imgRect = dragonRect

    def render(self):
        self.imgRect.center = self.x, self.y
        canvas.blit(self.img, self.imgRect)

    def update(self):
        if self.imgRect.bottom > fireRect.top:
            self.down = False
            self.up = True
        if self.imgRect.top < cactusRect.bottom:
            self.up = False
            self.down = True
        if self.down:
            self.y += Dragon.velocity
        if self.up:
            self.y -= Dragon.velocity
            
            
        

class Maryo:

    global cactusRect, fireRect

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.img = maryoImg
        self.imgRect = maryoRect
        
    def render(self):
        self.imgRect.center = self.x, self.y
        canvas.blit(self.img , self.imgRect)

    def update(self):

        if self.imgRect.top < cactusRect.bottom:
            gameOver()
        if self.imgRect.bottom > fireRect.top:
            gameOver()


def pauseMenu():

    pause = True

    while pause:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    terminate()
                elif event.key == pygame.K_p:
                    pause = False

        canvas.fill(white)
        displayText("Pause!!",black,50,"large")
        displayText("Press P to continue... or Q to quit...",black,150)

        pygame.display.update()
        clock.tick(5)

    
def gameLoop():

    global topScore
    score = 0
    moveY = 0
    speed = 20
    gravity = 20

    pygame.mixer.music.load("mario_theme.wav")
    pygame.mixer.music.play(-1)

    player = Maryo(50, screen_height/2)
    dragon = Dragon(screen_width - 50, screen_height/2)
    
    gravity = True

    flameList = []
    flameCounter = 0
    #addFlames = 20
    addFlames = random.randrange(30,40)
    
    while True:

        canvas.fill(black)

        if topScore < score:
            topScore = score
            
        level = checkLevel(score)


        flameCounter += 1

        if flameCounter == addFlames:
            if level == 1:
                addFlames = random.randrange(30,40)
            elif level == 2:
                addFlames = random.randrange(20,30)
            else:
                addFlames = random.randrange(10,20)
            flameCounter = 0
            newFlame = Flames(screen_width - 50, dragon.y)
            flameList.append(newFlame)

        for f in flameList:
            f.render()
            f.update()
            f.collision()

            if f.x <= 0:
                del f

        if level == 2:
               Flames.changeFlameSpeed(16)
        elif level == 3 or level == 4:
               Flames.changeFlameSpeed(20)        

        
        for event in pygame.event.get():
            score+=1
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                elif event.key == pygame.K_UP:
                    moveY -= speed
                    gravity = False
                    #score += 1
                elif event.key == pygame.K_DOWN:
                    moveY += speed
                    gravity = False
                    #score += 1
                elif event.key == pygame.K_p:
                    pauseMenu()
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    moveY = 0
                    gravity = True

        if gravity:
            moveY = 10
        player.y += moveY
        player.render()
        player.update()

        dragon.render()
        dragon.update()
        
        displayText("Score = "+str(score)+" || TopScore = "+str(topScore)+" || Level = "+str(level),white)
        pygame.display.update()
        clock.tick(fps)
    pygame.mixer.music.stop()

mainMenu()
gameLoop()
