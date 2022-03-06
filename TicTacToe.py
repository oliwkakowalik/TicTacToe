# libraries
import pygame as pg
import time
import sys
from pygame.locals import *

class TicTacToe:
    # storing the x or o value
    xo = 'x'
    # storing the winner's value
    winner = None
    # storing if game is a draw
    draw = None
    # width of the game window
    width = 400
    # height of the game window
    height = 400
    # colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    # setting fps
    fps = 30
    # tracking time
    CLOCK = pg.time.Clock()
    # 3 * 3 game board
    board = [[None] * 3, [None] * 3, [None] * 3]
    # infrastructure of the display
    screen = pg.display.set_mode((width, height + 100), 0, 32)
    # caption
    pg.display.set_caption("Tic tac toe")
    # images
    coverImage = pg.image.load("game_cover.jpg")
    xImage = pg.image.load("x.png")
    oImage = pg.image.load("o.png")
    # scale images
    coverImage = pg.transform.scale(coverImage, (width, height + 100))
    xImage = pg.transform.scale(xImage, (80, 80))
    oImage = pg.transform.scale(oImage, (80, 80))

    def printGameStatus(self):
        """
        function prints game status (message under the board)
        :return: None
        """
        if self.draw:
            message = "draw!"
        elif self.winner is None:
            message = self.xo.upper() + "'s turn!"
        else:
            message = self.winner.upper() + " won!"

        # font object
        font = pg.font.Font(None, 30)
        # font properties
        text = font.render(message, 1, self.white)
        # copy the rendered message onto the board
        # creating a small block at the bottom of the main display
        self.screen.fill((0, 0, 0), (0, 400, 500, 100))
        text_rect = text.get_rect(center=(self.width / 2, 500 - 50))
        self.screen.blit(text, text_rect)
        pg.display.update()

    def checkGameStatus(self):
        """
        function checks if somebody won or if there is a draw
        :return:
        """
        for row in range(0, 3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] and self.board[row][0] is not None:
                self.winner = self.board[row][0]
                pg.draw.line(self.screen, self.red, (30, (row + 1) * self.height / 3 - self.height / 6),
                             (self.width - 30, (row + 1) * self.height / 3 - self.height / 6), 4)
                break

        for col in range(0, 3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] is not None:
                self.winner = self.board[0][col]
                pg.draw.line(self.screen, self.red, ((col + 1) * self.width / 3 - self.width / 6, 30),
                             ((col + 1) * self.width / 3 - self.width / 6, self.height - 30), 4)
                break

        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] is not None:
            self.winner = self.board[0][0]
            pg.draw.line(self.screen, self.red, (50, 50), (350, 350), 4)

        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] is not None:
            self.winner = self.board[0][2]
            pg.draw.line(self.screen, self.red, (350, 50), (50, 350), 4)

        if all([all(row) for row in self.board]) and self.winner is None:
            self.draw = True

    def printXO(self, row: int, col: int):
        """
        function prints X/O image in the appropriate place
        :param row: number of clicked row
        :param col: number of clicked col
        :return: None
        """
        posX = self.width / 3 * (row - 1) + 30
        posY = self.height / 3 * (col - 1) + 30

        self.board[row - 1][col - 1] = self.xo

        if self.xo == 'x':
            self.screen.blit(self.xImage, (posY, posX))
            self.xo = 'o'
        else:
            self.screen.blit(self.oImage, (posY, posX))
            self.xo = 'x'

        pg.display.update()

    def catchClick(self):
        """
        function catches user click and decides where X/O image should be printed
        :return:
        """
        # get coordinates of mouse click
        x, y = pg.mouse.get_pos()

        # get col number
        col = int(x//(self.width / 3))+1
        # get row number
        row = int(y//(self.height / 3))+1
        row = row if row <= 3 else None

        if row and self.board[row - 1][col - 1] is None:
            self.printXO(row, col)
            self.checkGameStatus()
            self.printGameStatus()

    def initiateGameWindow(self):
        """
        functions initiates game window
        :return: None
        """
        # displaying over the screen
        self.screen.blit(self.coverImage, (0, 0))

        # updating the display
        pg.display.update()
        time.sleep(2)
        self.screen.fill(self.white)

        # drawing vertical lines
        pg.draw.line(self.screen, self.black, (self.width / 3, 0), (self.width / 3, self.height), 7)
        pg.draw.line(self.screen, self.black, (self.width / 3 * 2, 0), (self.width / 3 * 2, self.height), 7)

        # drawing horizontal lines
        pg.draw.line(self.screen, self.black, (0, self.height / 3), (self.width, self.height / 3), 7)
        pg.draw.line(self.screen, self.black, (0, self.height / 3 * 2), (self.width, self.height / 3 * 2), 7)
        self.printGameStatus()

    def resetGame(self):
        """
        function resets the gameplay
        :return: None
        """
        time.sleep(1.5)
        self.xo = 'x'
        self.draw = False
        self.winner = None
        self.board = [[None] * 3, [None] * 3, [None] * 3]
        self.initiateGameWindow()

    def play(self):
        """
        function is responsible for the gameplay
        :return: None
        """
        pg.init()
        self.initiateGameWindow()

        while True:
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONUP:
                    self.catchClick()
                    if self.winner or self.draw:
                        self.resetGame()
            pg.display.update()
            self.CLOCK.tick(self.fps)
