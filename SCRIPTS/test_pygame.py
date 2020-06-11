import traceback
import pygame
import chess.ChessBoard as cb
import py_game.GameObjects as go

scenario = 'castling1'

try:
    # Initialize board object
    board = cb.ChessBoard()

    if scenario == 'test':
        import chess.ChessPiece as cp
        # Initialize test chess pieces objects
        p1 = cp.Pawn('white', 'd8')
        k = cp.King('white', 'c4')
        r = cp.Bishop('black', 'd5')
        # Append pieces to board Object
        board.pieces.extend([p1, k, r])
    elif scenario == 'setup':
        # Set up board piece as new game
        board.setupBoard()
    elif scenario == 'castling1':
        # White cannot castle on either side because its king is in check
        import chess.ChessPiece as cp
        r1 = cp.Rook('white', 'a1', 'Queen')
        r2 = cp.Rook('white', 'h1', 'King')
        wk = cp.King('white', 'e1')
        q = cp.Queen('black', 'b4')
        bk = cp.King('black', 'e8')
        board.pieces.extend([r1, r2, bk, q, wk])
    elif scenario == 'castling2':
        import chess.ChessPiece as cp
        r1 = cp.Rook('white', 'a1', 'Queen')
        r2 = cp.Rook('white', 'h1', 'King')
        wk = cp.King('white', 'e1')
        q = cp.Queen('black', 'g7')
        bk = cp.King('black', 'e8')
        board.pieces.extend([r1, r2, bk, q, wk])


    # Initialize pygame object
    pygame.init()
    screen = pygame.display.set_mode((598,598))
    pygame.display.set_caption('Chess')

    # Initialize Board game object
    board = go.BoardGameObject(board)

    # Create a group of sprites with all the pieces of the board
    pieces_sprites = pygame.sprite.Group(tuple(board.pieces))

    # Create a list to store the moves sprites.
    moves_sprites = pygame.sprite.Group()

    # Draw everything for the first time
    # Paint background
    screen.fill((41,41,41))
    # Draw board
    screen.blit(board.image, board.rect)
    # Draw pieces on the screen
    pieces_sprites.draw(screen)
    # Update entire screen
    pygame.display.update()

    # The clock keeps the framerate at certain speed.
    clock = pygame.time.Clock()

    # Clear the events list. Needed to play by turns.
    pygame.event.clear()

    running = True
    selected_piece = None

    # main loop
    while running:
        clock.tick(30)

        event = pygame.event.wait()
        
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

        # handle MOUSEBUTTONDOWN
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            board.board.update()

            # get a list of all sprites that are under the mouse cursor
            clicked_piece = [p for p in pieces_sprites if p.rect.collidepoint(pos)]

            # If it clicks a possible move.
            clicked_move = [m for m in moves_sprites if m.rect.collidepoint(pos)]

            # board.board.update()

            can_play = False

            if len(clicked_piece) > 0 and len(clicked_move) > 0:
                if clicked_piece[0].piece.getColor() != board.board.getTurn():
                    can_play = True

            elif len(clicked_piece) > 0:
                if clicked_piece[0].piece.getColor() == board.board.getTurn():
                    can_play = True

            elif len(clicked_move) > 0:
                can_play = True

            
            if can_play:
                # If selected move has enemy piece == capture.
                if len(clicked_piece) > 0 and len(clicked_move) > 0:
                    piece = clicked_piece[0]
                    selected_piece.piece.capture(piece.piece)
                    pieces_sprites.remove(piece)
                    selected_piece = None
                    moves_sprites.empty()
                    board.board.toggleTurn()

                # Selects piece.
                elif len(clicked_piece) > 0:
                    if clicked_piece != selected_piece:
                        moves_sprites.empty()

                    print(clicked_piece[0].get_piece())
                    selected_piece = clicked_piece[0]

                    moves = board.board.possible_moves(clicked_piece[0].get_piece())

                    if len(moves) > 0:
                        moves_info = board.show_possible_moves(moves, clicked_piece[0].get_piece())
                        for m in moves_info:
                            moves_sprites.add(go.CellGameObject(type=m[2], coords=(m[0],m[1]), position=m[3]))
                            
                # Selected piece moves to new cell.
                elif len(clicked_move) > 0:
                    move = clicked_move[0]
                    selected_piece.piece.move(move.position)
                    selected_piece = None
                    moves_sprites.empty()
                    board.board.toggleTurn()

            # Clicked elsewhere, deselect piece.
            else:
                selected_piece = None
                moves_sprites.empty()

        # Paint background
        screen.fill((41,41,41))
        # Draw board
        screen.blit(board.image, board.rect)
        # Update pieces.
        pieces_sprites.update()
        # Draw pieces on the screen
        pieces_sprites.draw(screen)
        # Draw the possible moves
        moves_sprites.draw(screen)
        # Update entire screen
        pygame.display.update()

except Exception as e:
    print(traceback.format_exc())