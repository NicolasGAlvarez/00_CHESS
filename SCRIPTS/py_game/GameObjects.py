from chess.Utils import get_index_by_position, get_position_by_index
import chess.ChessBoard as cb
import pygame
from py_game.Utils import to_pygame, load_image, get_coords_by_position
from math import floor

class BoardGameObject:
    def __init__(self, board=None):
        # pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('Board.png')
        self.board = board
        self.pieces = []
        self.initialize_pieces_game_objects()

    def show_possible_moves(self, moves, piece):
        info = []

        for m in moves:
            type = 'move'

            if 'x' in m:
                m = m[m.find('x')+1:]
                type = 'capture'
            
            if '+' in m:
                m = m[:-1]
                type = 'check'

            if 'O-O-O' in m:
                rank = piece.getRank()
                m = f'a{rank}'
                type = 'castling'

            elif 'O-O' in m:
                rank = piece.getRank()
                m = f'h{rank}'
                type = 'castling'

            coords = get_coords_by_position(m)
            info.append((coords[0], coords[1], type, m))

        return info
            

    
    def initialize_pieces_game_objects(self):
        for p in self.board.pieces:
            self.pieces.append(PieceGameObject(p))


class PieceGameObject(pygame.sprite.Sprite):
    def __init__(self, piece):
        pygame.sprite.Sprite.__init__(self)
        self.piece = piece
        self.image_name = '{}_{}.png'.format(self.piece.getColor()[0], self.piece.getPiece())
        self.image, _ = load_image(self.image_name)
        self.coords = get_coords_by_position(self.piece.getPosition())
        self.rect = self.image.get_rect(center=self.coords)

    def get_piece(self):
        return self.piece

    def update(self):
        self.coords = get_coords_by_position(self.piece.getPosition())
        self.rect.centerx = self.coords[0]
        self.rect.centery = self.coords[1]



class CellGameObject(pygame.sprite.Sprite):
    def __init__(self, type=None, coords=None, position=None):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.image_name = f'cell_{self.type}.png'
        self.image, _ = load_image(self.image_name)

        if coords != None:
            self.coords = coords
            self.rect = self.image.get_rect(center=self.coords)

        if position != None:
            self.position = position