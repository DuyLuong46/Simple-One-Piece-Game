from graphics2 import *
import time
import random
import math
import sys
from playsound import playsound

ENEMY_SPEED = 5
HERO_SPEED = 50
FIREBALL_SPEED = 10
NUM_WIN = 15
STALL_TIME = 0.05
WINDOW_WIDTH = 666
WINDOW_HEIGHT = 666

def background(window):
    backgroundImg = Image(Point(WINDOW_WIDTH/2,WINDOW_HEIGHT/2), 'background.png')
    backgroundImg.draw(window)
    
    return backgroundImg

def button(window, x1, y1, x2, y2, color):
    button = Rectangle(Point(x1, y1), Point(x2, y2))
    button.setFill(color)
    button.draw(window)
    
    return button

def buttonText(window, button, text):
    buttonText = Text(button.getCenter(), text)
    buttonText.draw(window)
    
    return buttonText

def mainMenu(window):
    background(window)
    
    title = Text(Point(WINDOW_WIDTH / 2, 100), "Luffy vs Gecko Moria")
    title.setSize(36)
    title.setTextColor('white')
    title.setStyle('bold')
    title.draw(window)
    
    startButton = button(window, 250, 200, 400, 250, 'white')
    startButtonText = buttonText(window, startButton, 'Start Game')
    
    instructionsButton = button(window, 250, 300, 400, 350, 'white')
    instructionsButtonText = buttonText(window, instructionsButton, 'Instructions')
    
    quitButton = button(window, 250, 400, 400, 450, 'white')
    quitButtonText = buttonText(window, quitButton, 'Quit')

    return startButton, instructionsButton, quitButton, title, startButtonText, instructionsButtonText, quitButtonText

def instructionsMenu(window):
    background(window)
    
    instructionsText = Text(Point(WINDOW_WIDTH / 2, 100), "Instructions")
    instructionsText.setSize(24)
    instructionsText.setTextColor('white')
    instructionsText.setStyle('bold')
    instructionsText.draw(window)

    controls = Text(Point(WINDOW_WIDTH / 2, 200),
                    "Control Luffy, the hero, by clicking LEFT and RIGHT of the hero to move.\n"
                    "Press SPACE to shoot the devil fruit and defeat Gecko Maria,\n"
                    "or else he will steal your shadow.")
    controls.setTextColor('white')
    controls.setSize(16)
    controls.draw(window)
    
    backButton = button(window, 250, 350, 400, 400, 'white')
    backButtonText = buttonText(window, backButton, 'Back')

    return backButton

def createGameWindow():
    window = GraphWin("Gomu Gomu Nooo", WINDOW_WIDTH, WINDOW_HEIGHT)
    
    background(window)
    
    return window

def addEnemyToWindow(window):
    xPosition = random.randrange(15, WINDOW_WIDTH - 15)
    enemyImg = Image(Point(xPosition, 0), 'enemy.png')
    enemyImg.draw(window)
    return enemyImg

def addFireballToWindow(window, hero):
    fireballImg = Image(hero.getCenter(), 'balls.png')
    fireballImg.draw(window)
    return fireballImg

def moveEnemies(enemyImgList):
    for enemy in enemyImgList: 
        enemy.move(0, ENEMY_SPEED)
        
def moveFireballs(fireballs):
    for fireball in fireballs:
        fireball.move(0, -FIREBALL_SPEED)  # Move the fireball upwards

def moveHero(window, heroImg):
    mouseMove = window.checkMouse()
    heroCenter = heroImg.getCenter()
    heroX = heroCenter.getX()
    heroY = heroCenter.getY()
    
    heroHeight = heroImg.getHeight()
    heroHeightRadius = heroHeight / 2
    yMouseMax = heroY + heroHeightRadius
    yMouseMin = heroY - heroHeightRadius
    
    heroWidth = heroImg.getWidth()
    heroWidthRadius = heroWidth / 2
    xMouseMax = heroX + heroWidthRadius
    xMouseMin = heroX - heroWidthRadius
    
    if mouseMove is not None:
        xMouse = mouseMove.getX()
        yMouse = mouseMove.getY()
        if yMouse < yMouseMax and yMouse > yMouseMin:
            if xMouse > xMouseMax:
                heroImg.move(HERO_SPEED, 0)
            elif xMouse < xMouseMin:
                heroImg.move(-HERO_SPEED, 0)
                
def distanceBetweenPoints(point1, point2):
    dx = point2.getX() - point1.getX()
    dy = point2.getY() - point1.getY()                     
    return math.sqrt(dx**2 + dy**2)

def losingPoint(enemyImg, score, enemyList):
    enemyCenter = enemyImg.getCenter()
    enemyY = enemyCenter.getY() - enemyImg.getHeight() / 2
    
    if enemyY > WINDOW_HEIGHT:
        score -= 1
        enemyList.remove(enemyImg)  
    return score

def checkCollision(object1, object2):
    return distanceBetweenPoints(object1.getCenter(), object2.getCenter()) < 50  # Adjust collision threshold

def gameLoop(window, hero):
    score = 0
    missedEnemyCount = 0
    enemyList = []
    fireballs = []
    directions = Text(Point(333, 650), f'Points: {score}')
    directions.setSize(16)
    directions.setTextColor('white')
    directions.setStyle('bold')
    directions.draw(window)

    playsound('Background Music.mp3', False)    

    while True:
        
        if random.randrange(100) < 5:
            enemy = addEnemyToWindow(window)
            enemyList.append(enemy)
            
        moveEnemies(enemyList)
        moveFireballs(fireballs)

        for enemyImg in enemyList[:]:
            score = losingPoint(enemyImg, score, enemyList)
            directions.setText(f'Points: {score}')

            if checkCollision(hero, enemyImg):
                background(window)
                
                heroSad = Image(Point(WINDOW_WIDTH/2,WINDOW_HEIGHT/2), 'Sad Luffy.png')
                heroSad.draw(window)
                
                losingMessage = Text(Point(WINDOW_WIDTH / 2, 200),
                    "GAME OVER!\n"
                    "Oh no Luffy got caught :<\n"
                    "Now Gecko Moria is gonna steal your shadow.")

                losingMessage.setTextColor('white')
                losingMessage.setStyle('bold')
                losingMessage.setSize(26)
                losingMessage.draw(window)
                
                time.sleep(4)
                exit(1)

            for fireball in fireballs[:]:
                if checkCollision(fireball, enemyImg):
                    score += 1
                    directions.setText(f'Points: {score}')
                    enemyList.remove(enemyImg)
                    fireballs.remove(fireball)
                    enemyImg.undraw()
                    fireball.undraw()
                    break
        
        if window.checkKey() == 'space':
            fireball = addFireballToWindow(window, hero)
            fireballs.append(fireball)

        if score == NUM_WIN:
            background(window)
            
            heroHappy = Image(Point(WINDOW_WIDTH/2,WINDOW_HEIGHT/2), 'Happy Luffy.png')
            heroHappy.draw(window)
            
            winningMessage = Text(Point(WINDOW_WIDTH / 2, WINDOW_HEIGHT/2), "You win! You're the best! ")
            winningMessage.setSize(36)
            winningMessage.setTextColor('white')
            winningMessage.setStyle('bold')
            winningMessage.draw(window)
            
            break
        
        moveHero(window, hero)
        time.sleep(STALL_TIME)
        
    time.sleep(4)
    exit(1)

def main():
    window = GraphWin("Gomu Gomu Noooo!!!!!!", WINDOW_HEIGHT, WINDOW_WIDTH)
    window.setBackground("white")
    
    startButton, instructionsButton, quitButton, title, startText, instructionsText, quitText = mainMenu(window)
    
    while True:
        clickPoint = window.getMouse()
        
        if startButton.getP1().getX() < clickPoint.getX() < startButton.getP2().getX() and startButton.getP1().getY() < clickPoint.getY() < startButton.getP2().getY():
            window.close()
            gameWindow = createGameWindow( )
            hero = Image(Point(333, 580), "hero.png")
            hero.draw(gameWindow)
            gameLoop(gameWindow, hero)
            break

        elif instructionsButton.getP1().getX() < clickPoint.getX() < instructionsButton.getP2().getX() and instructionsButton.getP1().getY() < clickPoint.getY() < instructionsButton.getP2().getY():
            
            title.undraw()
            startButton.undraw()
            instructionsButton.undraw()
            quitButton.undraw()
            startText.undraw()
            instructionsText.undraw()
            quitText.undraw()
            
            backButton = instructionsMenu(window)

            while True:
                clickPoint = window.getMouse()
                if backButton.getP1().getX() < clickPoint.getX() < backButton.getP2().getX() and \
                   backButton.getP1().getY() < clickPoint.getY() < backButton.getP2().getY():
                    
                    window.clear()
                    startButton, instructionsButton, quitButton, title, startText, instructionsText, quitText = mainMenu(window)
                    break
                
        elif quitButton.getP1().getX() < clickPoint.getX() < quitButton.getP2().getX() and \
             quitButton.getP1().getY() < clickPoint.getY() < quitButton.getP2().getY():
             
             window.close()
             sys.exit(1)

main()