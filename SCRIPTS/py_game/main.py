import os
import chess.ChessBoard as cb
import chess.ChessPiece as cp
import PieceGameObject as pgo
import BoardGameObject as bgo

import traceback

RESOURCES_ROOT = 'C:\\Users\\Nico\\Code\\P5js\\00_CHESS\\RESOURCES'
IMG_ROOT = f'{RESOURCES_ROOT}\\IMG'

MOVE_COLOR = (100, 100, 255)
CAPTURE_COLOR = (255, 100, 100)
CHECK_COLOR = (255, 100, 255)

try:
    pygame.init()

    screen = pygame.display.set_mode((598,598))
    pygame.display.set_caption('Chess')

    board = cb.ChessBoard()
    board.setupBoard()
    # p1 = cp.Pawn('white', 'd8')
    # k = cp.King('white', 'c4')
    # r = cp.Bishop('black', 'd5')
    # board.pieces.extend([p1, k, r])
    board.printPieces()

    # Initialize list with all the game objects. Pass chess pieces objects in board as parameter.
    chess_pieces = []
    for p in board.pieces:
        chess_pieces.append(pgo.PieceGameObject(p))

    # Initialize Board game object
    board_bg = bgo.BoardGameObject(board)
    board_bg.set_pygame_img(pygame.image.load(f'{IMG_ROOT}\\{board_bg.get_img_source()}'))
    board_bg.set_img_rect(board_bg.get_pygame_img().get_rect(center=screen.get_rect().center))

    # Set image for pieces game objects
    for go in chess_pieces:
        go.set_pygame_img(pygame.image.load(f'{IMG_ROOT}\\{go.get_img_source()}'))
        go.set_img_rect(go.get_pygame_img().get_rect(center=board_bg.get_cell_coordinates(go.piece.getPosition())))

    
    # main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Paint background
        screen.fill((41,41,41))

        # Draw background
        screen.blit(board_bg.get_pygame_img(), board_bg.get_img_rect())

        # Draw chess pieces
        for go in chess_pieces:
            screen.blit(go.get_pygame_img(), go.get_img_rect())

        # handle MOUSEBUTTONUP
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            # get a list of all sprites that are under the mouse cursor
            clicked_piece = [p for p in chess_pieces if p.get_img_rect().collidepoint(pos)]
            if len(clicked_piece) > 0:
                clicked_piece = clicked_piece[0]
                print(clicked_piece.get_piece())

                moves = board_bg.board.possible_moves(clicked_piece.get_piece())
                
                if len(moves) > 0:
                    board_bg.show_possible_moves(moves)
                    pygame.draw.rect(screen,color,(x,y,board_bg.cell_size,board_bg.cell_size))
            

        pygame.display.update()
except Exception as e:
    print(traceback.format_exc())