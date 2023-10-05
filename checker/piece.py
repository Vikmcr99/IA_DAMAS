from .values import  WHITE, SQUARE, GREY, KING, BLACK
import pygame

class Piece:
    PADDING = 18
    BORDER = 2

    def __init__(self, row, column, color):
        self.row = row
        self.column = column
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.pos_piece_square()

    def pos_piece_square(self): #calculate the position of the piece
        self.x = SQUARE * self.column + SQUARE // 2
        self.y = SQUARE * self.row + SQUARE // 2

    def checker_king(self):
        self.king = True
    
    def drawPiece(self, square):
        circle = SQUARE//2 - self.PADDING
        pygame.draw.circle(square, self.color, (self.x, self.y), circle)
        if self.king:
            square.blit(KING, (self.x - KING.get_width()//2, self.y - KING.get_height()//2))

    def move(self, row, column):
        self.row = row
        self.column = column
        self.pos_piece_square()

