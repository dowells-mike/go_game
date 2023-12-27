"""Piece is an Enumerated class which will make distinguishing the Stones easier"""


class Piece(object):
    NoPiece = 0  # 0 represents no piece on the board.
    Black = 1  # 1 represents black pieces.
    White = 2  # 2 represents white pieces. Another alternative could be -1, but 2 is used to avoid complexity.
