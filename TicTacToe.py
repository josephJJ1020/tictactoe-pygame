import sys
import random
import time
import time as t

import pygame
from pygame import *

pygame.init()
pygame.font.init()


screensize = screenwidth, screenheight = 500, 500
screen = pygame.display.set_mode((screensize))

logo = pygame.image.load("x.png")
pygame.display.set_caption("Tic Tac Toe")
pygame.display.set_icon(logo)

font = pygame.font.SysFont("arial", 500//3, bold=True) # Initialize fonts
fontsmall = pygame.font.SysFont("rockwell", 50)
fontsmaller = pygame.font.SysFont("arial", 20)

black = (0, 0, 0)  # Instantiate colors
white = (255, 255, 255)
red = (255, 0, 0)
orange = (255,165,0)
yellow = (255, 255, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


screen.fill(white)  # Draw background
squaresize = 500 // 3

counter = 1  # Will be used for changing characters (X or O)

class Square:
    def __init__(self, coordinates, color):
        self.coordinates = coordinates
        self.color = color
        self.char = None
        self.clicked = False
        self.square = pygame.draw.rect(screen, color, (coordinates[0], coordinates[1], squaresize, squaresize))

    def reset(self):
        self.square = pygame.draw.rect(screen, self.color, (self.coordinates[0], self.coordinates[1], squaresize, squaresize))

def gameloop():
    global counter
    square1 = Square((0, 0), white)
    square2 = Square((squaresize, 0), white)
    square3 = Square((squaresize * 2, 0), white)
    square4 = Square((0, squaresize), white)
    square5 = Square((squaresize, squaresize), white)
    square6 = Square((squaresize * 2, squaresize), white)
    square7 = Square((0, squaresize * 2), white)
    square8 = Square((squaresize, squaresize * 2), white)
    square9 = Square((squaresize * 2, squaresize * 2), white)

    squarelist = [square1, square2, square3, square4, square5, square6, square7, square8, square9]
    winners = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1 , 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]  # Win conditions


    def drawLines():  # Draw screen lines to visually divide the board
        pygame.draw.line(screen, orange, [squaresize, 0], [squaresize, 500])
        pygame.draw.line(screen, orange, [squaresize * 2, 0], [squaresize * 2, 500])
        pygame.draw.line(screen, orange, [0, squaresize], [500, squaresize])
        pygame.draw.line(screen, orange, [0, squaresize * 2], [500, squaresize * 2])


    def drawGrid():  # Reset board
        for square in squarelist:
            square.char = None
            square.clicked = False
            square.reset()


    def drawtext(loc):  # Draws X or Y
        global counter
        loc.char = character
        text = font.render(loc.char, True, white if loc.color == black else black)
        textrect = text.get_rect()
        textrect.center = loc.square.center
        screen.blit(text, textrect)
        loc.clicked = True
        counter += 1
        print(counter)


    def drawWinner(char):  # Draw winner popup
        winnercircle = pygame.draw.circle(screen, red, (screenwidth // 2, screenheight // 2), 150)
        winnertext = fontsmall.render(f"{char} wins!", True, white)
        winnerrect = winnertext.get_rect()
        winnerrect.center = (screenwidth // 2, screenheight // 2)
        screen.blit(winnertext, winnerrect)


    def checkwinner():
        global counter
        for square in winners:

            if all(squarelist[x].char == "O" for x in square):
                char = "O"
                for tile in squarelist:
                    tile.clicked = True
                drawWinner(char)

                for event in pygame.event.get():  # To be able to exit during winner screen
                    if event.type == pygame.QUIT:
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:  # Redraw the board and clear the characters
                            counter = 1
                            drawGrid()
                            drawLines()

            elif all(squarelist[x].char == "X" for x in square):  # Checks if X wins based on win conditions
                char = "X"
                for tile in squarelist:
                    tile.clicked = True
                drawWinner(char)

                for event in pygame.event.get():  # To be able to exit during winner screen
                    if event.type == pygame.QUIT:
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:  # Redraw the board and clear the characters
                            counter = 1
                            drawGrid()
                            drawLines()

            elif not opensquare and all([tile.char for tile in squarelist]):
                winnercircle = pygame.draw.circle(screen, red, (screenwidth // 2, screenheight // 2), 150)
                winnertext = fontsmall.render("Tie!", True, white)
                winnerrect = winnertext.get_rect()
                winnerrect.center = (screenwidth // 2, screenheight // 2)
                screen.blit(winnertext, winnerrect)

                for event in pygame.event.get():  # To be able to exit during winner screen
                    if event.type == pygame.QUIT:
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:  # Redraw the board and clear the characters
                            counter = 1
                            drawGrid()
                            drawLines()

    while True:
        drawLines()
        opensquare = [i for i in squarelist if not i.clicked]
        checkwinner()

        character = "X" if not counter % 2 == 0 else "O"
        pos = pygame.mouse.get_pos()

        if counter % 2 == 0 and opensquare:
            pcpick = random.choice(opensquare)
            # pygame.time.wait(1000)
            drawtext(pcpick)
            opensquare.remove(pcpick)

        elif counter % 1 == 0 and opensquare:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        counter = 1
                        drawGrid()

                for tile in squarelist:
                    if event.type == pygame.MOUSEBUTTONDOWN and tile.square.collidepoint(pos):
                        if not tile.clicked:
                            drawtext(tile)
                            opensquare.remove(tile)
                        else:
                            print("clicked already!")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.update()


def mainmenu():
    screen.fill(orange)
    menu = pygame.draw.rect(screen, white, [100, 100, 300, 300])

    text = fontsmall.render("Tic Tac Toe", True, black)
    textrect = text.get_rect()
    textrect.center = (screenwidth//2, screenheight//2)
    screen.blit(text, textrect)

    enter = fontsmaller.render("press Enter to play", True, black)
    enterrect = enter.get_rect()
    enterrect.bottom, enterrect.x = 310, 180
    screen.blit(enter, enterrect)

    quit = fontsmaller.render("press Escape to quit", True, black)
    quitrect = quit.get_rect()
    quitrect.bottom, quitrect.x = 330, 175
    screen.blit(quit, quitrect)
    pygame.display.update()


if __name__ == "__main__":
    mainmenu()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameloop()
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

