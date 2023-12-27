# Import necessary modules from PyQt6
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel, QDialog, QFrame
from piece import Piece

# Function to handle the skipping turn event
def passevent():
    print("Pass clicked")

# ScoreBoard class, a subclass of QDockWidget
class ScoreBoard(QDockWidget):
    # Constants for color representation
    BLACK_COLOR = QColor(Qt.GlobalColor.black).name()
    WHITE_COLOR = QColor(Qt.GlobalColor.white).name()

    # Constructor to initialize the scoreboard with player names
    def __init__(self, player1_name, player2_name):
        super().__init__()
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.initUI()

    # Method to initialize the UI of the scoreboard
    def initUI(self):
        # Set properties of the scoreboard
        self.setFixedWidth(300)
        self.setFixedHeight(778)
        self.setWindowTitle('ScoreBoard')
        self.setStyleSheet("""
            background-color: #f2f2f2;
            color: #333;
            font-family: Lucida Sans;
        """)

        # Create main widget, layout, and labels for the scoreboard
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()
        self.instructions = self.create_label("Instructions\n 1. Click anywhere to place"
                                              "\n a piece \n 2. Press ctrl+S or P to pass a turn \n 3. Press ctrl+r or R to reset the Game")
        self.player_turn = self.create_label(f"{self.player1_name}  ")
        self.timerLeft = self.create_label("Time remaining: ")
        self.label_playerStatus = self.create_label("Players Status")
        self.label_PrisonersBlack = self.create_label(f"{self.player1_name} Prisoners: ")
        self.label_PrisonersWhite = self.create_label(f"{self.player2_name} Prisoners: ")
        self.label_TerritoriesBlack = self.create_label(f"{self.player1_name} Territory: ")
        self.label_TerritoriesWhite = self.create_label(f"{self.player2_name} Territory: ")

        # Set layout for the main widget
        self.mainWidget.setLayout(self.mainLayout)
        self.add_widgets_to_layout()

        # Set the main widget for the scoreboard
        self.setWidget(self.mainWidget)

    # Helper method to create a QLabel with specified text
    def create_label(self, text):
        label = QLabel(text)
        label.setMargin(10)
        return label

    # Helper method to add widgets to the layout
    def add_widgets_to_layout(self):
        widgets = [self.instructions, self.player_turn, self.timerLeft, self.label_playerStatus,
                   self.label_PrisonersBlack, self.label_PrisonersWhite, self.label_TerritoriesBlack,
                   self.label_TerritoriesWhite]

        for widget in widgets:
            self.mainLayout.addWidget(widget)
            self.mainLayout.addSpacing(15)

    # Method to establish connections between the scoreboard and the game board
    def make_connection(self, board):
        board.TO_TIME.connect(self.setTimeRemaining)
        board.captives.connect(self.updatePrisoners)
        board.territories.connect(self.updateTerritories)
        board.notifier.connect(self.displaynotification)
        board.player_turn.connect(self.updateturn)

    # Slot method to update the remaining time on the scoreboard
    @pyqtSlot(int)
    def setTimeRemaining(self, timeRemainng):
        update = "Time Remaining:" + str(timeRemainng) + " sec"
        self.timerLeft.setText(update)

    # Slot method to update the current player's turn on the scoreboard
    def updateturn(self, player):
        if player == 1:
            self.player_turn.setText(f"Current Turn: {self.player1_name}")
        elif player == 2:
            self.player_turn.setText(f"Current Turn: {self.player2_name}")

    # Slot method to update the count of prisoners for each player on the scoreboard
    def updatePrisoners(self, n, Player):
        if Player == Piece.Black:
            update = f"{self.player1_name} Prisoners: " + n
            self.label_PrisonersBlack.setText(update)
        elif Player == Piece.White:
            update = f"{self.player2_name} prisoners: " + n
            self.label_PrisonersWhite.setText(update)

    # Slot method to update the count of territories for each player on the scoreboard
    def updateTerritories(self, n, Player):
        if Player == Piece.Black:
            update = f"{self.player1_name} territory: " + n
            self.label_TerritoriesBlack.setText(update)
        elif Player == Piece.White:
            update = f"{self.player2_name} territory: " + n
            self.label_TerritoriesWhite.setText(update)

    # Slot method to display a notification dialog on the scoreboard
    def displaynotification(self, message):
        dialog = QDialog(self)
        dialog.setFixedWidth(300)
        dialog.setWindowTitle("Notification")
        layout = QVBoxLayout()
        layout.addWidget(QLabel(message))
        dialog.setLayout(layout)
        dialog.exec()


