from chess import ChessPiece as cp
from chess.Utils import get_index_by_position, get_position_by_index

class ChessBoard:
    def __init__(self):
        self.pieces = []
        self.turn = 'white'
        self.check = False
        self.state = None

    
    def update(self):
        if len(self.pieces) == 0: # if no pieces in board setup new game.
            self.setupBoard()
            self.turn = 'white'
            print('[NEW MATCH]')
            self.state = f'[{self.turn.upper()}] Move.'
        else:
            checking_pieces = self.get_pieces_checking()
            if len(checking_pieces) > 0: # Is king in check?
                self.check = True
                self.state = f'[{self.turn.upper()}] In check.'
                if self.is_check_mate():
                    self.state = f'[GAME OVER]'
            else:
                self.check = False
                self.state = f'[{self.turn.upper()}] Move.'
        print(self.state)



    def toggleTurn(self):
        '''
            Toggles current turn. From white to black.
            :return: None
        '''
        self.turn = 'black' if self.turn == 'white' else 'white'


    def populate(self, color):
        '''
            Instantiates and positions pieces for given color.
            :param color: str
            :return: None
        '''
        if color == 'white':
            row1 = '1'
            row2 = '2'
        elif color == 'black':
            row1 = '8'
            row2 = '7'

        k = cp.King(color, 'e'+row1)
        q = cp.Queen(color, 'd'+row1)
        b1 = cp.Bishop(color, 'c'+row1)
        b2 = cp.Bishop(color, 'f'+row1)
        n1 = cp.Knight(color, 'b'+row1)
        n2 = cp.Knight(color, 'g'+row1)
        r1 = cp.Rook(color, 'a'+row1, side='queen')
        r2 = cp.Rook(color, 'h'+row1, side='king')

        self.pieces.extend([k,q,b1,b2,n1,n2,r1,r2])

        for i in range(0,8):
            p = cp.Pawn(color, chr(97+i)+str(row2))
            self.pieces.append(p)


    def getTurn(self):
        return self.turn


    def getPieces(self):
        return self.pieces


    def printPieces(self):
        for c in self.pieces:
            print(c)


    def setupBoard(self):
        '''
            Populates board with pieces for new game.
            :return: None
        '''
        self.populate('white')
        self.populate('black')


    def get_piece_by_position(self, position):
        '''
            Returns piece in given position.
            :param position: str
            :return: ChessPiece
        '''
        for p in self.pieces:
            if p.getPosition() == position:
                return p


    def possible_moves(self, piece, seethrough):
        '''
            Return possible moves for given piece.
            :param piece: ChessPiece
            :return: list<str>
        '''
        moves = []
        
        piece_direction = piece.getDirection()
        piece_file = piece.getFile()
        piece_rank = piece.getRank()

        if piece.getPiece() == 'Pawn':
            # at edge of the board?
            if (piece_rank == 8 and piece_direction == 1) or (piece_rank == 1 and piece_direction == -1):
                return moves

            next_cell = f'{piece_file}{int(piece_rank)+1*piece_direction}'
            next_cell_2 = f'{piece_file}{int(piece_rank)+2*piece_direction}'

            capture_cells = []
            if piece_file != 'a':
                capture_cells.append(f'{chr(ord(piece_file)-1)}{int(piece_rank)+1*piece_direction}')
            if piece_file != 'h':
                capture_cells.append(f'{chr(ord(piece_file)+1)}{int(piece_rank)+1*piece_direction}')
            
            move_forward = self.can_move_to_cell(piece, next_cell, False)
            if len(move_forward) > 0:
                moves.extend(move_forward)
                move_forward = self.can_move_to_cell(piece, next_cell_2, False)
                if len(move_forward) > 0 and not piece.hasMoved(): # move to spaces
                    moves.extend(move_forward)

            for c in capture_cells: # capture diagonally
                is_enemy_in_cell, enemy_piece = self.is_enemy_piece_in_cell(c, piece.getColor())
                if is_enemy_in_cell:
                    if enemy_piece.getPiece() == 'King':
                        moves.append(f'x{c}+')
                    else:
                        moves.append(f'x{c}')
            
        elif piece.getPiece() == 'Rook':
            moves.extend(self.can_move_inline(piece, 'forward', True, seethrough))
            moves.extend(self.can_move_inline(piece, 'back', True, seethrough))
            moves.extend(self.can_move_inline(piece, 'right', True, seethrough))
            moves.extend(self.can_move_inline(piece, 'left', True, seethrough))

        elif piece.getPiece() == 'Bishop':
            moves.extend(self.can_move_diagonally(piece, 'forward_right', True, seethrough))
            moves.extend(self.can_move_diagonally(piece, 'forward_left', True, seethrough))
            moves.extend(self.can_move_diagonally(piece, 'back_right', True, seethrough))
            moves.extend(self.can_move_diagonally(piece, 'back_left', True, seethrough))

        elif piece.getPiece() == 'Knight':
            for i in [-2,-1,1,2]:
                for j in [-2,-1,1,2]:
                    if abs(i)!=abs(j):
                        next_file = chr(ord(piece_file)-i*piece_direction)
                        next_rank = int(piece_rank)-j*piece_direction

                        if self.is_within_board(next_file, next_rank):
                            next_cell = '{}{}'.format(next_file, next_rank)
                            moves.extend(self.can_move_to_cell(piece, next_cell, True))

        elif piece.getPiece() == 'Queen':
            moves.extend(self.can_move_inline(piece, 'forward', True, seethrough))
            moves.extend(self.can_move_inline(piece, 'back', True, seethrough))
            moves.extend(self.can_move_inline(piece, 'right', True, seethrough))
            moves.extend(self.can_move_inline(piece, 'left', True, seethrough))

            moves.extend(self.can_move_diagonally(piece, 'forward_right', True, seethrough))
            moves.extend(self.can_move_diagonally(piece, 'forward_left', True, seethrough))
            moves.extend(self.can_move_diagonally(piece, 'back_right', True, seethrough))
            moves.extend(self.can_move_diagonally(piece, 'back_left', True, seethrough))

        elif piece.getPiece() == 'King':
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    if not (i==0 and j==0):
                        next_cell = '{}{}'.format(chr(ord(piece_file)-i*piece_direction), int(piece_rank)-j*piece_direction)
                        king_next_cell = self.get_surrounding_enemies(next_cell)
                        king_next_cell = [e for e in king_next_cell if e.getPiece() == 'King']
                        if not king_next_cell:
                            if not self.are_cells_attacked([next_cell], self.turn, True):
                                moves.extend(self.can_move_to_cell(piece, next_cell, True))

            # Castlings
            moves.extend(self.can_castle(piece, 'King'))
            moves.extend(self.can_castle(piece, 'Queen'))

        return moves


    def get_surrounding_enemies(self, cell):
        file = cell[0]
        rank = cell[1]

        pieces = []

        for i in [-1,0,1]:
                for j in [-1,0,1]:
                    if not (i==0 and j==0):
                        next_cell = '{}{}'.format(chr(ord(file)-i), int(rank)-j)
                        piece = self.get_piece_by_position(next_cell)
                        if piece:
                            if piece.getColor() != self.turn:
                                pieces.append(piece)
        
        return pieces


    def can_castle(self, king, side):
        moves = []

        # Check if king has not moved and isnt currently in check.
        if king.hasMoved() or self.check:
            return moves

        # Get rook. Alive, not moved, same color.
        rook = [p for p in self.pieces if p.getPiece() == 'Rook' and p.getSide() == side and p.isAlive() and p.getColor() == king.getColor() and not p.hasMoved()]

        if len(rook) == 0:
            return moves

        rank = king.getRank()

        if side == 'King':
            empty_cells = [f'f{rank}',f'g{rank}']
            attacked_cells = [f'f{rank}',f'g{rank}']
        elif side == 'Queen':
            empty_cells = [f'b{rank}', f'c{rank}',f'd{rank}']
            attacked_cells = [f'c{rank}',f'd{rank}']

        # Check if cells between king and rook are empty.
        if not self.are_cells_empty(empty_cells):
            return moves
        
        # Check if king pass through or ends up in an attacked cell.
        if self.are_cells_attacked(attacked_cells, king.getColor(), False):
            return moves

        if side == 'King':
            moves.append('O-O')
        else:
            moves.append('O-O-O')

        return moves


    def are_cells_attacked(self, cells, color, seethrough):
        '''
            Check if given cells are being attacked by rival piece.
            :param cell: list<str>
            :param color: str
            :return: bool
        '''
        rival_color = 'white' if color == 'black' else 'black'
        rival_pieces = [p for p in self.pieces if p.isAlive() and p.getColor() == rival_color and p.getPiece() != 'King']

        attacked = None
        for r in rival_pieces:
            moves = self.possible_moves(r, seethrough)
            attacked = [c for c in cells if c in moves]
            if len(attacked) > 0:
                return True 

        return False

    
    def is_cell_empty(self, cell):
        '''
            Check if given cell is empty.
            :param cell: str
            :return: bool
        '''
        is_empty = True
        for p in self.pieces:
            if p.getPosition() == cell and p.isAlive() == True:
                is_empty = False
                break
        return is_empty

    
    def are_cells_empty(self, cells):
        '''
            Check if given cells are empty.
            :param cell: list<str>
            :return: bool
        '''
        is_empty = True
        for p in self.pieces:
            if p.getPosition() in cells and p.isAlive() == True:
                is_empty = False
                break
        return is_empty


    def is_enemy_piece_in_cell(self, cell, color):
        '''
            Check if given cell has enemy piece.
            :param cell: str
            :param color: str
            :return: bool, ChessPiece
        '''
        has_enemy = False
        enemy_piece = None
        for p in self.pieces:
            if p.getPosition() == cell and p.isAlive() == True and p.getColor() != color:
                has_enemy = True
                enemy_piece = p
                break
        return has_enemy, enemy_piece

    
    def can_move_to_cell(self, piece, dest_cell, can_capture):
        '''
            Check if given piece can move to given cell.
            :param piece: ChessPiece
            :param dest_cell: str
            :param can_capture: bool
            :return: list<str>
        '''
        moves = []

        if not self.is_within_board(dest_cell[0], dest_cell[1]):
            return moves
        
        if self.is_cell_empty(dest_cell):
            moves.append(dest_cell)
        elif can_capture:
            is_enemy_in_cell, enemy_piece = self.is_enemy_piece_in_cell(dest_cell, piece.getColor())
            if is_enemy_in_cell:
                if enemy_piece.getPiece() == 'King':
                    moves.append(f'x{dest_cell}+')
                else:
                    moves.append(f'x{dest_cell}')

        return moves


    def can_move_inline(self, piece, move_direction, can_capture, seethrough):
        '''
            Check if given piece can move to spaces vertically and horizontally.
            :param piece: ChessPiece
            :param move_direction: int
            :param can_capture: bool
            :param seethrough: bool
            :return: list<str>
        '''
        moves = []

        piece_file = piece.getFile()
        piece_rank = piece.getRank()
        piece_direction = piece.getDirection()

        scan = True
        step = 0
        while scan:
            step += 1

            if move_direction == 'forward':
                next_cell = '{}{}'.format(piece_file, int(piece_rank)+step*piece_direction)
            elif move_direction == 'back':
                next_cell = '{}{}'.format(piece_file, int(piece_rank)-step*piece_direction)
            elif move_direction == 'right':
                next_cell = '{}{}'.format(chr(ord(piece_file)+step), piece_rank)
            elif move_direction == 'left':
                next_cell = '{}{}'.format(chr(ord(piece_file)-step), piece_rank)

            # if next_cell not within board then break the loop
            if not self.is_within_board(next_cell[0], next_cell[1]):
                break

            if seethrough: # get possible moves as if piece is the only one in the board.
                moves.append(next_cell)
            else:
                if self.is_cell_empty(next_cell):
                    moves.append(next_cell)
                elif can_capture:
                    is_enemy_in_cell, enemy_piece = self.is_enemy_piece_in_cell(next_cell, piece.getColor())
                    if is_enemy_in_cell:
                        if enemy_piece.getPiece() == 'King':
                            moves.append(f'x{next_cell}+')
                        else:
                            moves.append(f'x{next_cell}')
                    scan = False
                else:
                    scan = False
        
        return moves


    def can_move_diagonally(self, piece, move_direction, can_capture, seethrough):
        '''
            Check if given piece can move to spaces diagonally.
            :param piece: ChessPiece
            :param move_direction: int
            :param can_capture: bool
            :return: list<str>
        '''
        moves = []

        piece_file = piece.getFile()
        piece_rank = piece.getRank()
        piece_direction = piece.getDirection()

        scan = True
        step = 0
        while scan:
            step += 1

            if move_direction == 'forward_right':
                next_cell = '{}{}'.format(chr(ord(piece_file)+step*piece_direction), int(piece_rank)+step*piece_direction)
            elif move_direction == 'forward_left':
                next_cell = '{}{}'.format(chr(ord(piece_file)-step*piece_direction), int(piece_rank)+step*piece_direction)
            elif move_direction == 'back_right':
                next_cell = '{}{}'.format(chr(ord(piece_file)+step*piece_direction), int(piece_rank)-step*piece_direction)
            elif move_direction == 'back_left':
                next_cell = '{}{}'.format(chr(ord(piece_file)-step*piece_direction), int(piece_rank)-step*piece_direction)

            # if next_cell not within board then break the loop
            if not self.is_within_board(next_cell[0], next_cell[1]):
                break
            
            if seethrough: # get possible moves as if piece is the only one in the board.
                moves.append(next_cell)
            else:
                if self.is_cell_empty(next_cell):
                    moves.append(next_cell)
                elif can_capture:
                    is_enemy_in_cell, enemy_piece = self.is_enemy_piece_in_cell(next_cell, piece.getColor())
                    if is_enemy_in_cell:
                        if enemy_piece.getPiece() == 'King':
                            moves.append(f'x{next_cell}+')
                        else:
                            moves.append(f'x{next_cell}')
                    scan = False
                else:
                    scan = False
            
        return moves


    def is_within_board(self, file, rank):
        '''
            Check if given position (file, rank) is within board limits.
            :param file: str
            :param rank: str
            :return: bool
        '''
        if not (97 <= ord(file) <= 104) or not (1 <= int(rank) <= 8):
            return False
        else:
            return True

    
    def get_pieces_checking(self):
        # Get rival pieces moves, search for pieces with check possible moves '+'.
        rival_pieces = [p for p in self.pieces if p.getColor() != self.turn and p.isAlive()]

        check_pieces = []
        for rival in rival_pieces:
            moves = self.possible_moves(rival, False)
            check_move = [m for m in moves if '+' in m]
            if len(check_move) > 0:
                check_pieces.append(rival)

        return check_pieces

    
    def is_check_mate(self):
        pieces_checking = self.get_pieces_checking()

        king = [k for k in self.pieces if k.getPiece() == 'King' and k.getColor() == self.turn]
        king = king[0]

        can_king_move = self.possible_moves(king, False)
        
        if len(can_king_move) > 0:
            return False

        for check in pieces_checking:
            position = check.getPosition()
            if self.are_cells_attacked(position, self.turn, False):
                return False

        return True