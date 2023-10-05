import pygame
from .values import WHITE, GREEN, SQUARE,BLACK, RED, GREY, SILK, DARKBLUE, BLUE
from checker.board import Board

class Game:
    def __init__(self, square):
        self.chosen = None
        self.board = Board()
        self.turn = BLACK
        self.valid_moves = {}
        self.square = square
    
    def resetGame(self):
        self.__init__()
    
    def updateBoard(self):
        self.board.drawBoard(self.square)
        self.drawMoves(self.valid_moves)
        pygame.display.update()


    def winner(self):
        return self.board.winner()


    def chosenPiece(self, row, column):
        if self.chosen:
            result = self._move(row, column)
            if not result: #If the select piece cant move, i call the method again
                self.chosen = None
                self.chosenPiece(row, column)
        
        piece = self.board.selectedPiece(row, column)
        if piece != 0 and piece.color == self.turn: # If the select piece is ok
            self.chosen = piece
            self.valid_moves = self.board.validMoves(piece)
            return True
            
        return False
    
    def changePlayer(self):
        self.valid_moves = {}
        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK

    def get_board(self):
        return self.board

    def moves_AI(self, board):
        self.board = board
        self.changePlayer()

    def _move(self, row, column):
        piece = self.board.selectedPiece(row, column)
        if self.chosen and piece == 0 and (row, column) in self.valid_moves: # Check if the move is possible
            self.board.move(self.chosen, row, column)
            jump = self.valid_moves[(row, column)]
            if jump:
                self.board.removePiece(jump)
            self.changePlayer()
        else:
            return False

        return True

    def drawMoves(self, moves):
        for m in moves:
            row, column = m
            
            if self.turn == BLACK:
                pygame.draw.circle(self.square, DARKBLUE, (column * SQUARE + SQUARE//2, row * SQUARE + SQUARE//2), 20) 
            else:
                pygame.draw.circle(self.square, RED, (column * SQUARE + SQUARE//2, row * SQUARE + SQUARE//2), 20)
            

