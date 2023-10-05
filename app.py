import pygame
from checker.values import WIDTH, HEIGHT, SQUARE, WHITE, BLACK, BLUE, COLUMNS, BROWN, RED
from checker.game import Game
from intelligent_agent.minimax import MiniMax
pygame.font.init()



FPS = 60


SET = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('AI Checker')

def main():
    game_state = "start_menu"
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


        if game_state == "start_menu":
            draw_start_menu()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_F1]:
                game_state = "player_mode"
                game = Game(SET)
            if keys[pygame.K_F2]:
                game_state = "AI_mode"
                game = Game(SET)

        
        if game_state == "player_mode":
            if game.winner() != None:
                print(game.winner())
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    row, col = mouse_event(position)
                    game.chosenPiece(row, col)
            
            game.updateBoard()
            
        if game_state == "AI_mode":
            if game.turn == WHITE:
                value, new_board = MiniMax(game.get_board(), 3, WHITE, game)
                game.moves_AI(new_board)
            
            if game.winner() != None:
                print(game.winner())
                run = False


            if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    row, col = mouse_event(position)
                    game.chosenPiece(row, col)
            
            game.updateBoard()
            
    
    pygame.quit()

def mouse_event(position):
    x, y = position
    row = y // 100  # if the x or y was 435 or something like that, the square will be the square  number 4
    col = x // 100
    return row, col

def draw_start_menu():
    SET.fill(BLUE)
    for row in range(8):
        for column in range(row % 2, COLUMNS, 2): #basically the mod will be between (0,1) -> On line 0, its starts with white. On line 1, its starts with blue..
            pygame.draw.rect(SET, WHITE , (row*SQUARE, column *SQUARE, SQUARE, SQUARE))
    font = pygame.font.SysFont('comicsansms', 80)
    title = font.render("WELCOME", True, BLACK)
    player_mode = font.render('F1 - player vs player', True, BLACK)
    AI_mode = font.render('F2 - AI vs player', True, BLACK)
    SET.blit(title, (WIDTH/2 - title.get_width()/2, HEIGHT/5 - title.get_height()/5))
    SET.blit(player_mode, (WIDTH/2 - player_mode.get_width()/2, HEIGHT/3 + player_mode.get_height()/3))
    SET.blit(AI_mode, (WIDTH/3 - AI_mode.get_width()/3.1, HEIGHT/2 + AI_mode.get_height()/2))
    pygame.display.update()
    

main()