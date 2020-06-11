class ChessPiece:
    color = None
    position = None
    alive = True
    piece = None
    identifier = None


    def __repr__(self):
        return {'piece':self.piece, 'color':self.color, 'position':self.position, 'alive':self.alive}


    def __str__(self):
        return f'Piece:{self.piece}, Color:{self.color}, Position:{self.position}, Alive:{self.alive}'


    def move(self, newPos):
        '''
            Updates chess piece position
            :param newPos: str
            :return: str
        '''
        self.position = newPos


    def capture(self, capturedPiece):
        '''
            Captures given ChessPiece and updates position.
            :param capturedPiece: ChessPiece
            :return: str
        '''
        if capturedPiece.isAlive():
            capturedPiece.setAlive(False)
            self.move(capturedPiece.getPosition())


    def getPosition(self):
        return self.position


    def isAlive(self):
        return self.alive


    def setAlive(self, value):
        self.alive = value


    def getColor(self):
        return self.color


    def getIdentifier(self):
        return self.identifier


    def getPiece(self):
        return self.piece


    def getFile(self):
        if self.position != None:
            return self.position[0]


    def getRank(self):
        if self.position != None:
            return self.position[1]


    def getDirection(self):
        if self.color == 'white':
            return 1
        elif self.color == 'black':
            return -1 


     

class King(ChessPiece):
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.piece = 'King'
        self.identifier = 'K'
        self.moved = False
        self.check = False
        

    def hasMoved(self):
        return self.moved


    def isInCheck(self):
        return self.check


    def setCheck(self, value):
        self.check = value


    def move(self, newPos):
        '''
            Updates king position and moved attribute.
            :param newPos: str
            :return: str
        '''
        super().move(newPos)
        if not self.moved:
            self.moved = True


    def capture(self, capturedPiece):
        '''
            Captures given ChessPiece and updates position and moved attribute.
            :param capturedPiece: ChessPiece
            :return: str
        '''
        super().capture(capturedPiece)
        if not self.moved:
            self.moved = True




class Queen(ChessPiece):
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.piece = 'Queen'
        self.identifer = 'Q'
        self.img = f'{self.color[0]}_QUEEN.png'




class Bishop(ChessPiece):
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.piece = 'Bishop'
        self.identifier = 'B'
        self.img = f'{self.color[0]}_BISHOP.png'




class Knight(ChessPiece):
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.piece = 'Knight'
        self.identifier = 'N'
        self.img = f'{self.color[0]}_KNIGHT.png'




class Rook(ChessPiece):
    def __init__(self, color, position, side=None):
        self.color = color
        self.position = position
        self.piece = 'Rook'
        self.identifier = 'R'
        self.img = f'{self.color[0]}_ROOK.png'
        self.moved = False
        self.side = side


    def getSide(self):
        return self.side


    def hasMoved(self):
        return self.moved


    def move(self, newPos):
        '''
            Updates rook position and moved attribute.
            :param newPos: str
            :return: str
        '''
        super().move(newPos)
        if not self.moved:
            self.moved = True


    def capture(self, capturedPiece):
        '''
            Captures given ChessPiece and updates position and moved attribute.
            :param capturedPiece: ChessPiece
            :return: str
        '''
        super().capture(capturedPiece)
        if not self.moved:
            self.moved = True




class Pawn(ChessPiece):
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.piece = 'Pawn'
        self.identifier = 'P'
        self.moved = False
        self.img = f'{self.color[0]}_PAWN.png'


    def hasMoved(self):
        return self.moved


    def move(self, newPos):
        '''
            Updates pawn position and moved attribute.
            :param newPos: str
            :return: str
        '''
        super().move(newPos)
        if not self.moved:
            self.moved = True


    def capture(self, capturedPiece):
        '''
            Captures given ChessPiece and updates position and moved attribute.
            :param capturedPiece: ChessPiece
            :return: str
        '''
        super().capture(capturedPiece)
        if not self.moved:
            self.moved = True