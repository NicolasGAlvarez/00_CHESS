from chess import ChessPiece as cp
from chess import ChessBoard as cb
import re

"""
    States
        Idle
        Executing
        Finished
"""

class Game:
    def __init__(self, board, game_data):
        self.board = board
        self.game_data = game_data
        self.state = 'Idle'
        self.id = game_data.get('game_id')
        self.moves = game_data.get('game_moves')
        self.moves_count = len(self.moves)
        self.current_move_index = 0
        self.current_move = self.moves[self.current_move_index]
        self.current_player = 'white'
        self.winner = None


    def play(self):
        if self.state == 'Idle':
            self.state = 'Executing'
            while self.current_move_index < self.moves_count:
                move_done = self.execute(self.current_move)
                if move_done:
                    self.current_move_index += 1
                    if self.current_player == 'white':
                        self.current_player = 'black'
                    else:
                        self.current_player = 'white'
                else:
                    self.state = 'Break'
                    print('Game break.')
                    return

            self.state = 'Finished'
            return
        elif self.state == 'Finished':
            print('Game already finished')


    def execute(self, move_to_execute):
        # Leer proxima jugada
        # primera jugada siempre es jugador blanco
        # d4 : Mueve peon en file d (posicion d2) a rank 4 (posicion d4)

        # Movida legal?
        if self.is_legal_move(move_to_execute):
            return True
        else:
            print(f'Illegal move {move_to_execute}')
            return False

    
    def is_legal_move(self, move):
        play_match, is_check, is_checkmate, is_prom, prom_piece = self.identify_move(move)

        # Moves only legal to empty space.

        print('Aca')

        # if the cell is empty and its not a capture then its illegal
        # empty_space = self.board.is_space_empty(destination_space)

        # if first letter is uppercase then get identifier
        # if move[0].isupper():
        #     pass
        # else: # No identifier, then pawn.
        #     if is_capture: 
        #         pass
        #     elif not is_capture: # if it's not a capture then can only move forward
        #         # search current board for a pawn for that player in that file (column)
        #         available_pieces = self.board.get_pawns_by_file(self.current_player, move[0])
        #         legal_move, available_pieces = self.board.get_closest_pawn(self.current_player, available_pieces, move)


    def identify_move(self, move):
        pattern1 = '\\b[a-h][1-8]\\b' # Pawn moves
        pattern2 = '\\b[a-h]x[a-h][1-8]\\b' # Pawn captures
        pattern3 = '\\b[KQBNR][a-h][1-8]\\b' # Special piece moves
        pattern4 = '\\b[KQBNR]x[a-h][1-8]\\b' # Special piece captures
        pattern5 = '\\b[KQBNR][a-h]x[a-h][1-8]\\b' # Special identified piece captures
        pattern6 = '\\bO-O-O\\b' # King castling
        pattern7 = '\\bO-O\\b' # Queen castling

        pattern8 = '+' # Check
        pattern9 = '#' # Checkmate
        pattern10 = '=' # Promotion

        patterns = {
            'pawn_moves':pattern1
            , 'pawn_captures':pattern2
            , 'special_moves':pattern3
            , 'special_captures':pattern4
            , 'identified_captures':pattern5
            , 'queen_castling': pattern6
            , 'king_castling': pattern7
            }

        play_match = None
        is_check = False
        is_checkmate = False
        is_prom = False
        prom_piece = None

        for item in patterns.items():
            result = re.match(item[1], move)
            
            if result != None:
                play_match = item[0]
                print(item[0], move)
                break
        
        if pattern8 in move:
            is_check = True
            print('Check')

        if pattern9 in move:
            checkmate_match = True
            print('Checkmate')

        if pattern10 in move:
            prom_match = True
            prom_piece = move[move.find(pattern10)+1]
            print(f'Promotion ({prom_piece})')

        if play_match == 'pawn_moves': # pawn
            board_file = move[0]
            piece_match = self.board.get_pawn_by_file(self.current_player, board_file)
            destination_cell = move

        elif play_match == 'pawn_captures':
            board_file = move[2]
            piece_match = self.board.get_pawn_by_file(self.current_player, board_file)
            destination_cell = move[2:3]

        elif play_match == 'special_moves': # Gotta check which special can move to the destination
            board_file = move[1]
            destination_cell = move[1:2]
            special_identifier = move[0]
            piece_match = self.board.get_special_by_destination(self.current_player, destination_cell)

        return play_match, is_check, is_checkmate, is_prom, prom_piece