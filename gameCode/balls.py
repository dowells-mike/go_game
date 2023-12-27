# Import the Piece class from a module called "Piece"
from piece import Piece


class Balls(object):
    # Set to none since the board starts with 0 pieces.
    Piece = Piece.NoPiece
    liberties = 0
    # x and y are set to -1 because the board is a 8x8 board but only a 7x7 part of it is functional. So we take into
    # account that offset.
    x = -1
    y = -1

    def __init__(self, Piece, x, y):
        # initialising the constructor
        self.Piece = Piece
        self.liberties = 0
        self.x = x
        self.y = y

    def get_piece(self):
        # Return the value of the Piece attribute for the instance
        return self.Piece

    def get_liberties(self):
        # Return the value of the liberties attribute for the instance
        return self.liberties

    def set_liberties(self, liberties):
        # Set the value of the liberties attribute for the instance
        self.liberties = liberties

    def get_top(self, boardArray):
        # Getting the stone above the current one.
        if self.y == 0:
            # If this piece is at the top of the board, return None
            return None
        else:
            # Otherwise, return the stone above this one in the boardArray
            return boardArray[self.y - 1][self.x]

    def get_right(self, boardArray):
        # Getting the stone to the right of the current one.
        if self.x == 6:
            # If this piece is at the right edge of the board, return None
            return None
        else:
            # Otherwise, return the piece to the right of this one in the boardArray
            return boardArray[self.y][self.x + 1]

    def get_left(self, boardArray):
        # Getting the stone to the left of the current one.
        if self.x == 0:
            # If this piece is at the left edge of the board, return None
            return None
        else:
            # Otherwise, return the piece to the left of this one in the boardArray
            return boardArray[self.y][self.x - 1]

    def get_down(self, boardArray):
        # Getting the stone to the right of the current one.
        if self.y == 6:
            # If this piece is at the bottom of the board, return None
            return None
        else:
            # Otherwise, return the piece below this one in the boardArray
            return boardArray[self.y + 1][self.x]

