import pygame
import tkinter as tk
from tkinter import messagebox
from .values import BLACK, ROWS, SQUARE, COLUMNS, WHITE, BLUE, RED
from .piece import Piece


class Board:
    def __init__(self):
        self.board = []
        self.remainBlack = 12
        self.remainWhite = 12
        self.blackKings = 0
        self.whiteKings = 0
        self.maxDepth = 10
        self.createBoard()

    def drawBoard(self, square):
        self.drawSquares(square)
        for row in range(8):
            for column in range(8):
                piece = self.board[row][column]
                if piece != 0:
                    piece.drawPiece(square)
    
    def drawSquares(self, square):
        square.fill(BLUE)
        for row in range(8):
            for column in range(row % 2, COLUMNS, 2): #basically the mod will be between (0,1) -> On line 0, its starts with white. On line 1, its starts with blue..
                pygame.draw.rect(square, WHITE , (row*SQUARE, column *SQUARE, SQUARE, SQUARE))

    def move(self, piece, row, column):
        #swap elements in a list reversing their elements
        #This way i can move a piece and catch the new position of that piece in the board (after the move)
        self.board[piece.row][piece.column], self.board[row][column] = self.board[row][column], self.board[piece.row][piece.column]
        piece.move(row, column)

        if row == 7 or row == 0:
            piece.checker_king()
            if piece.color == WHITE:
                self.whiteKings += 1
            else:
                self.blackKings += 1 

    def selectedPiece(self, row, column):
        return self.board[row][column]

    def createBoard(self):
        for row in range(8):
            self.board.append([])
            for column in range(COLUMNS):
                if column % 2 == ((row +  1) % 2): #To define what square will have a piece or not
                    if row < 3:
                        self.board[row].append(Piece(row, column, WHITE)) #whites on rows 0,1,2
                    elif row > 4:
                        self.board[row].append(Piece(row, column, BLACK))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
        

    def removePiece(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.column] = 0
            if piece != 0:
                if piece.color == BLACK:
                    self.remainBlack -= 1
                else:
                    self.remainWhite -= 1
    
    def wndMessage(self, message):
        root = tk.Tk()
        root.wm_withdraw()
        msgBox = messagebox.showinfo(message)
        if msgBox == "ok":
            root.destroy()
            pygame.quit()
            
            
   
    def winner(self):
        if self.remainBlack <= 0:
            msg = self.wndMessage("WHITE WON THE GAME!")
            
        elif self.remainWhite <= 0:
            msg = self.wndMessage("BLACK WON THE GAME!")
        
        return None 
    
    def validMoves(self, piece):
        save_moves = {}
        left = piece.column - 1
        right = piece.column + 1
        row = piece.row
        column = piece.column

        if piece.color == BLACK or piece.king: #move up
            save_moves.update(self._jump_left(row -1, max(row-3, -1), -1, piece.color, left))
            save_moves.update(self._jump_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king: #move down
            save_moves.update(self._jump_left(row +1, min(row+3, 8), 1, piece.color, left))
            save_moves.update(self._jump_right(row +1, min(row+3, 8), 1, piece.color, right))
    
        return save_moves
    
    def diagonalSquares(self, column,row):
        x1 = column + 1 #right
        x2 = column - 1 #left
        y1 = row + 1    #down
        y2 = row - 1    # up
        moves = [(x1,y2),(x2,y2),(x1,y1),(x2,y1)] #[upper right, upper left, down right, down left]
        return moves
        

    def _jump_left(self, start, stop, step, color, left, jump_piece=[]): #check if is possible jump over a piece and if is possible double jumped or triple jumped
        save_moves = {}
        jump_again = []
        for r in range(start, stop, step):
            if left < 0: #if left <0 is no longer more columns for the left
                break
            
            current = self.board[r][left]
            
            if current == 0: #empty square -> valid move
                if jump_piece and not jump_again:
                    break
                elif jump_piece: # its how the dictonary will save the double jumped or triple jumped 
                    save_moves[(r, left)] =  jump_piece + jump_again 
                else:
                    save_moves[(r, left)] = jump_again #jump again is a empty list so, in this case the move is valid but we do not jump over anything
                
                if jump_again: #double jumped or triple jumped
                    if step == -1:# move up
                        row = max(r-3, -1) # r-3 = 2 rows up || -1 = end of board (upside)
                    else: # move down
                        row = min(r+3, 8) # r+3 = 2 rows down || 8 = end of board (downside)
                    save_moves.update(self._jump_left(r+step, row, step, color, left-1,jump_piece=jump_again))
                    save_moves.update(self._jump_right(r+step, row, step, color, left+1,jump_piece=jump_again))
                break
            
            elif current.color == color: #cannot jump the piece that is the same color
                break
            
            else:
                jump_again = [current] #the move is possible if the square after the jump is empty -> so, loop again

            left -= 1
        
        return save_moves

    def _jump_right(self, start, stop, step, color, right, jump_piece=[]): #same method as _jump_left but for right
        save_moves = {}
        jump_again = []
        for r in range(start, stop, step):
            if right >= 8:
                break
            
            current = self.board[r][right]
            if current == 0:
                if jump_piece and not jump_again:
                    break
                elif jump_piece:
                    save_moves[(r,right)] =  jump_piece + jump_again
                else:
                    save_moves[(r, right)] = jump_again
                
                if jump_again:
                    if step == -1:
                        row = max(r-3, -1)
                    else:
                        row = min(r+3, 8)
                    save_moves.update(self._jump_left(r+step, row, step, color, right-1,jump_piece=jump_again))
                    save_moves.update(self._jump_right(r+step, row, step, color, right+1,jump_piece=jump_again))
                break
            elif current.color == color:
                break
            else:
                jump_again = [current]

            right += 1
        
        return save_moves
    
    def evaluateBoard(self): #score the board to minimax, to select the best option
        return self.remainWhite - self.remainBlack + (self.whiteKings * 1.5 - self.blackKings * 1.5)

    def get_by_color(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces
    
    