from copy import deepcopy
from checker.values import BLACK, WHITE
from checker.board import Board
import pygame

def get_possible_moves(board, color, game): #check all possibles moves from the current position
    moves = []
    for piece in board.get_by_color(color): #loop through all pieces of tha same color on the board
        valid_moves = board.validMoves(piece) #check the valid moves for them
        for move, jump in valid_moves.items():
            tempBoard = deepcopy(board) #deepcopy makes a copy without being changed if the origial one was
            tempPiece = tempBoard.selectedPiece(piece.row, piece.column)
            newBoard = simulate_AI_moves(tempPiece, move, tempBoard, game, jump)
            moves.append(newBoard)
    
    return moves


def simulate_AI_moves(piece, move, board, game, jump):
    board.move(piece, move[0], move[1]) #move the piece to the row and column tested by the get_possible_moves function
    if jump:
        board.removePiece(jump)

    return board

def MiniMax(board, deep, maximize, game):
    if deep == 0 or board.winner() != None: #Last node of the tree
        return board.evaluateBoard(), board #return the evaluate of the current position
    
    if maximize: #white player
        maxEvaluation = float('-inf') #if we did not check nothing yet, the current best is -Inf
        bestMove = None
        for move in get_possible_moves(board, WHITE, game):
            score = MiniMax(move, deep-1, False, game)[0] #decrease the depth to make a recursive call until deep==0, then return the evaluation to define the best move
            maxEvaluation = max(maxEvaluation, score)
            if maxEvaluation == score:
                bestMove = move
        
        return maxEvaluation, bestMove
    else: #minmize
        minEvaluation = float('inf')
        bestMove = None
        for move in get_possible_moves(board, BLACK, game):
            score = MiniMax(move, deep-1, True, game)[0]
            minEvaluation = min(minEvaluation, score)
            if minEvaluation == score:
                bestMove = move
        
        return minEvaluation, bestMove






