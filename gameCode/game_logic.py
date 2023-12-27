# Import necessary classes from other modules
from piece import Piece
from balls import Balls

class GameEngine:
    turn = Piece.Black
    x_position = 0
    y_position = 0
    board_array = 0
    captive_is_white = 0
    captive_is_black = 0
    territories_is_white = 0
    territories_is_black = 0

    def update_params(self, board_array, x_position, y_position):
        self.x_position = x_position
        self.y_position = y_position
        self.board_array = board_array

    def position_not_occupied(self):
        if self.board_array[self.y_position][self.x_position].Piece == Piece.NoPiece:
            return True
        else:
            return False

    def toggle_turns(self):
        if self.turn == Piece.Black:
            self.turn = Piece.White
        else:
            self.turn = Piece.Black

    def plot_the_balls(self):
        if self.turn == Piece.Black:
            self.board_array[self.y_position][self.x_position].Piece = Piece.Black
        else:
            self.board_array[self.y_position][self.x_position].Piece = Piece.White

    def update_liberty(self):
        count = 0
        for row in self.board_array:
            for cell in row:
                count = 0
                if cell.Piece != Piece.NoPiece:
                    piece_color = cell.Piece

                    if cell.get_top(self.board_array) is not None and (cell.get_top(self.board_array).Piece == piece_color or cell.get_top(self.board_array).Piece == Piece.NoPiece):
                        count = count + 1
                    if cell.get_right(self.board_array) is not None and (cell.get_right(self.board_array).Piece == piece_color or cell.get_right(self.board_array).Piece == Piece.NoPiece):
                        count = count + 1
                    if cell.get_left(self.board_array) is not None and (cell.get_left(self.board_array).Piece == piece_color or cell.get_left(self.board_array).Piece == Piece.NoPiece):
                        count = count + 1
                    if cell.get_down(self.board_array) is not None and (cell.get_down(self.board_array).Piece == piece_color or cell.get_down(self.board_array).Piece == Piece.NoPiece):
                        count = count + 1
                    cell.set_liberties(count)

    def update_captives(self):
        for row in self.board_array:
            for cell in row:
                if cell.liberties == 0 and cell.Piece != Piece.NoPiece:
                    if cell.Piece == Piece.Black:
                        self.captive_is_white = self.captive_is_white + 1
                        self.board_array[cell.y][cell.x] = Balls(Piece.NoPiece, cell.x, cell.y)
                        return "Black Ball Captured "
                    elif cell.Piece == Piece.White:
                        self.captive_is_black = self.captive_is_black + 1
                        self.board_array[cell.y][cell.x] = Balls(Piece.NoPiece, cell.x, cell.y)
                        return "White Ball Captured "

    def update_captives_the_second(self):
        # Check neighboring cells and capture pieces if necessary
        if self.board_array[self.y_position][self.x_position].get_top(self.board_array) is not None and self.board_array[self.y_position][
            self.x_position].get_top(self.board_array).liberties == 0 and self.board_array[self.y_position][
            self.x_position].get_top(self.board_array).Piece != Piece.NoPiece:
            return self.capture_piece(self.x_position, self.y_position - 1)
        elif self.board_array[self.y_position][self.x_position].get_right(self.board_array) is not None and self.board_array[self.y_position][
            self.x_position].get_right(self.board_array).liberties == 0 and self.board_array[self.y_position][
            self.x_position].get_right(self.board_array).Piece != Piece.NoPiece:
            return self.capture_piece(self.x_position + 1, self.y_position)
        elif self.board_array[self.y_position][self.x_position].get_left(self.board_array) is not None and self.board_array[self.y_position][
            self.x_position].get_left(self.board_array).liberties == 0 and self.board_array[self.y_position][
            self.x_position].get_left(self.board_array).Piece != Piece.NoPiece:
            return self.capture_piece(self.x_position - 1, self.y_position)
        elif self.board_array[self.y_position][self.x_position].get_down(self.board_array) is not None and self.board_array[self.y_position][
            self.x_position].get_down(self.board_array).liberties == 0 and self.board_array[self.y_position][
            self.x_position].get_down(self.board_array).Piece != Piece.NoPiece:
            return self.capture_piece(self.x_position, self.y_position + 1)

    def capture_piece(self, x, y):
        if self.board_array[y][x].Piece == Piece.Black:
            self.captive_is_white = self.captive_is_white + 1
            self.board_array[y][x] = Balls(Piece.NoPiece, x, y)
            return "Black Ball Captured "
        elif self.board_array[y][x].Piece == Piece.White:
            self.captive_is_black = self.captive_is_black + 1
            self.board_array[y][x] = Balls(Piece.NoPiece, x, y)
            return "White Ball Captured "
        
    def is_bad_move(self):
        oppositeplayer = 0
        if self.turn == Piece.Black:
            oppositeplayer = Piece.White
        else:
            oppositeplayer = Piece.Black
        count = 0

        # Check adjacent cells and count how many belong to the opposite player
        if self.board_array[self.y_position][self.x_position].get_top(self.board_array) is None or self.board_array[self.y_position][
            self.x_position].get_top(self.board_array).Piece == oppositeplayer:
            count = count + 1
        if self.board_array[self.y_position][self.x_position].get_left(self.board_array) is None or self.board_array[self.y_position][
            self.x_position].get_left(self.board_array).Piece == oppositeplayer:
            count = count + 1
        if self.board_array[self.y_position][self.x_position].get_right(self.board_array) is None or self.board_array[self.y_position][
            self.x_position].get_right(self.board_array).Piece == oppositeplayer:
            count = count + 1
        if self.board_array[self.y_position][self.x_position].get_down(self.board_array) is None or self.board_array[self.y_position][
            self.x_position].get_down(self.board_array).Piece == oppositeplayer:
            count = count + 1

        # Check if the move is considered bad based on the surrounding conditions
        if count == 4:
            if self.board_array[self.y_position][self.x_position].get_top(self.board_array) is not None and self.board_array[self.y_position][
                self.x_position].get_top(self.board_array).liberties == 1:
                return False
            if self.board_array[self.y_position][self.x_position].get_left(self.board_array) is not None and \
                    self.board_array[self.y_position][
                        self.x_position].get_left(self.board_array).liberties == 1:
                return False
            if self.board_array[self.y_position][self.x_position].get_right(self.board_array) is not None and \
                    self.board_array[self.y_position][
                        self.x_position].get_right(self.board_array).liberties == 1:
                return False
            if self.board_array[self.y_position][self.x_position].get_down(self.board_array) is not None and \
                    self.board_array[self.y_position][
                        self.x_position].get_down(self.board_array).liberties == 1:
                return False
            return True
        else:
            return False
    

    
    def get_black_prisoner(self):
        return str(self.captive_is_white)

    def get_white_prisoner(self):
        return str(self.captive_is_black)

    def get_black_territories(self):
        return str(self.territories_is_black)

    def get_white_territories(self):
        return str(self.territories_is_white)

    def update_territories(self):
        # Count the number of positions occupied by each player
        count1 = 0
        count2 = 0
        for row in self.board_array:
            for cell in row:
                if cell.Piece == Piece.Black:
                    count1 = count1 + 1
                elif cell.Piece == Piece.White:
                    count2 = count2 + 1
        # Update the territories for both players
        self.territories_is_white = count2
        self.territories_is_black = count1
        
    def return_the_scores(self, Piece):
        if Piece == Piece.Black:
            return self.captive_is_white + self.territories_is_black
        elif Piece == Piece.White:
            return self.captive_is_black + self.territories_is_white

   

