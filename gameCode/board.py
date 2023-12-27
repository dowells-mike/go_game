# Import necessary modules
from collections import namedtuple
from copy import copy
from PyQt6.QtWidgets import QFrame, QStatusBar, QMessageBox
from PyQt6.QtCore import Qt, QBasicTimer, pyqtSignal, QPoint
from PyQt6.QtGui import QPainter, QBrush, QColor
from piece import Piece
from balls import Balls
from game_logic import GameEngine
from PyQt6.QtCore import QCoreApplication

# Define the GameBoard class
class GameBoard(QFrame):
    # Class constants
    BOARD_WIDTH = 7
    BOARD_HEIGHT = 7
    TIMER_SPEED = 1000  # This is set to 1 second
    COUNTER = 120  # The time allowed before a game over is 2 minutes
    passcount = 0  # Used to keep track of how many turns have been skipped consecutively
    game_engine = GameEngine()  # we will need the GameEngine class
    TO_TIME = pyqtSignal(int)  # This will be used for the timer events
    TO_CLICK = pyqtSignal(str)  # This will be used for the clicking events
    captives = pyqtSignal(str, int)
    territories = pyqtSignal(str, int)
    notifier = pyqtSignal(str)
    player_turn = pyqtSignal(int)

    # The constructor
    def __init__(self, parent):
        super().__init__(parent)
        self.board_array = None
        self.is_started = None
        self.timer = None
        self.init_board()
        self.game_states = []

    # Initialising the board
    def init_board(self):
        # Initialize timer, started status, and game engine
        self.timer = QBasicTimer()
        self.is_started = False
        self.start()
        # Create a 2D array representing the game board with Balls
        self.board_array = [[Balls(Piece.NoPiece, i, j) for i in range(self.BOARD_WIDTH)] for j in
                            range(self.BOARD_HEIGHT)]
        self.game_engine = GameEngine()

    # Helper method to get the width of a square
    def square_width(self):
        return self.contentsRect().width() / self.BOARD_WIDTH

    # Helper method to get the height of a square
    def square_height(self):
        return self.contentsRect().height() / self.BOARD_HEIGHT

    # Start the game
    def start(self):
        self.is_started = True
        self.reset_game()
        # Start the timer to track game time
        self.timer.start(self.TIMER_SPEED, self)

    # Handle timer events
    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            if self.COUNTER == 0:
                self.game_over()
            else:
                # Update the game time counter
                self.COUNTER -= 1
                self.TO_TIME.emit(self.COUNTER)
        else:
            super(GameBoard, self).timerEvent(event)

    # Draw the game board and pieces
    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_board(painter)
        self.draw_pieces(painter)

    # Handle mouse clicks
    def mousePressEvent(self, event):
        # Convert mouse click positions to board coordinates
        click_loc = f"click location [{event.position().x()},{event.position().y()}]"
        self.mouse_positions(event)
        # Emit a signal with the click location
        self.TO_CLICK.emit(click_loc)

    # Convert mouse positions to board coordinates
    def mouse_positions(self, event):
        x_position, y_position = event.position().x(), event.position().y()
        x_coordinate, y_coordinate = x_position / self.square_width(), y_position / self.square_height()
        x, y = round(x_coordinate) - 1, round(y_coordinate) - 1
        # Update game engine parameters based on the clicked position
        self.game_engine.update_params(self.board_array, x, y)
        # Check if the move is allowed and place the ball
        if self.is_move_allowed():
            self.place_ball()
            self.update_territories_and_captives()
        self.update()

    # Draw the game board
    def draw_board(self, painter):
        color = QColor(169, 169, 169)
        color2 = QColor(211, 211, 211)
        brush = QBrush(Qt.BrushStyle.SolidPattern)
        brush.setColor(color)
        for row in range(0, self.BOARD_HEIGHT):
            for col in range(0, self.BOARD_WIDTH):
                painter.save()
                col_transformation, row_transformation = self.square_width() * col, self.square_height() * row
                painter.translate(col_transformation, row_transformation)
                painter.fillRect(col, row, round(self.square_width()), round(self.square_height()), brush)
                painter.restore()
                brush.setColor(color2 if brush.color() == color else color)

    # Draw the game pieces
    def draw_pieces(self, painter):
        for row in range(len(self.board_array)):
            for col in range(len(self.board_array[0])):
                painter.save()
                painter.translate((self.square_width() * row) + self.square_width() * 0.70,
                                  (self.square_height() * col) + self.square_height() * 0.70)
                color = self.get_piece_color(row, col)
                painter.setPen(color)
                painter.setBrush(color)
                radius = self.square_width() / 3
                center = QPoint(round(radius), round(radius))
                painter.drawEllipse(center, round(radius), round(radius))
                painter.restore()

    # Get the color of a game piece
    def get_piece_color(self, row, col):
        piece = self.board_array[col][row].Piece
        if piece == Piece.NoPiece:
            return QColor(Qt.GlobalColor.transparent)
        elif piece == Piece.White:
            return QColor(Qt.GlobalColor.white)
        elif piece == Piece.Black:
            return QColor(Qt.GlobalColor.black)

    # Check if the current player's move is allowed
    def is_move_allowed(self):
        if self.game_engine.position_not_occupied():
            if self.game_engine.is_bad_move():
                self.notify_user("Move not Allowed")
                return False
            return True
        else:
            self.notify_user("Spot Occupied")
            return False

    # Place a game ball on the board
    def place_ball(self):
        # Update the game engine and handle captures, liberties, and territories
        self.game_engine.plot_the_balls()
        self.game_engine.update_liberty()
        message = self.game_engine.update_captives_the_second()
        if message is not None:
            self.notify_user(message)
            self.game_engine.update_liberty()
        self.game_engine.update_territories()
        self.update_states()
        # Check for KO and change turns
        if not self.check_KO():
            self.passcount = 0
            self.change_turn()
        else:
            self.handle_ko()

    # Update the game states
    def update_states(self):
        self.game_states.append(self.copy_board())

    # Remove previous game states
    def remove_states(self, previous_state):
        for row_index, row in enumerate(previous_state):
            for col_index, cell in enumerate(row):
                self.board_array[row_index][col_index] = Balls(cell.Piece, col_index, row_index)

    # Copy the current game board
    def copy_board(self):
        return [[Balls(cell.Piece, i, j) for i, cell in enumerate(row)] for j, row in enumerate(self.board_array)]

    # Check if KO rule is triggered
    def check_KO(self):
        try:
            if self.assert_boards_are_equal(self.game_states[-1], self.game_states[-3]):
                self.notify_user('KO. Revert back now')
                return True
        except IndexError:
            pass
        return False

    # Assert if two game boards are equal
    def assert_boards_are_equal(self, current, previous):
        return all(cell.Piece == current[row][col].Piece for row, row_cells in enumerate(previous) for col, cell in
                   enumerate(row_cells))

    # Change the turn to the next player
    def change_turn(self):
        self.game_engine.toggle_turns()
        self.COUNTER = 120
        self.player_turn.emit(self.game_engine.turn)

    # Update territories and captives signals
    def update_territories_and_captives(self):
        self.captives.emit(str(self.game_engine.get_black_prisoner()), Piece.Black)
        self.captives.emit(str(self.game_engine.get_white_prisoner()), Piece.White)
        self.territories.emit(str(self.game_engine.get_white_territories()), Piece.White)
        self.territories.emit(str(self.game_engine.get_black_territories()), Piece.Black)

    # Check and announce the winner
    def check_winner(self):
        black_score, white_score = self.game_engine.return_the_scores(Piece.Black), self.game_engine.return_the_scores(
            Piece.White)
        self.notify_user(f"Scores : \n Black : {black_score}\n White : {white_score}")
        if black_score > white_score:
            self.notify_user("Black Wins")
        elif black_score < white_score:
            self.notify_user("White Wins")
        else:
            self.notify_user("Game is a Draw")

    # Get the score for a specific player
    def get_score(self, Piece):
        return self.game_engine.return_the_scores(Piece)

    # Notify the user with a message
    def notify_user(self, message):
        self.notifier.emit(message)

    # Reset the game to its initial state
    def reset_game(self):
        self.notify_user("Game Reset")
        # Reset the game board and game engine parameters
        self.board_array = [[Balls(Piece.NoPiece, i, j) for i in range(self.BOARD_WIDTH)] for j in
                            range(self.BOARD_HEIGHT)]
        self.game_engine.black_prisoner = 0
        self.game_engine.white_prisoner = 0
        self.game_engine.black_territories = 0
        self.game_engine.white_territories = 0
        self.game_engine.turn = Piece.Black
        self.timer.stop()
        self.COUNTER = 120
        self.timer.start(self.TIMER_SPEED, self)

    # Skip the current player's turn
    def skip_turn(self):
        self.notify_user("Move Passed")
        self.passcount += 1
        self.change_turn()
        if self.passcount == 2:
            self.notify_user("Double turn skipped, game over")
            self.check_winner()
            return True
        return False

    # Handle game over event
    def game_over(self):
        self.notify_user("Timer Ran out : Game over")
        winner = "White Player Wins" if self.game_engine.turn == Piece.Black else "Black Player Wins"
        self.notify_user(winner)
        reply = QMessageBox.question(self, 'Game Over', f"{winner}\nDo you want to play a new game?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.reset_game()
        else:
            QCoreApplication.instance().quit()

    # Function to handle the KO Rule
    def handle_ko(self):
        if self.game_engine.turn == Piece.White:
            self.game_engine.captive_is_white -= 1
        else:
            self.game_engine.captive_is_black -= 1
        self.remove_states(self.game_states[-2])
        self.game_engine.update_liberty()
        self.game_engine.update_territories()
        self.update_states()
