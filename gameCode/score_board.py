from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel, QDialog, QFrame
from PyQt6.QtCore import pyqtSlot
from piece import Piece


def passevent():
    print("Pass clicked")



class ScoreBoard(QDockWidget):
    BLACK_COLOR = QColor(Qt.GlobalColor.black).name()
    WHITE_COLOR = QColor(Qt.GlobalColor.white).name()

    def __init__(self, player1_name, player2_name):
        super().__init__()
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.initUI()

    def initUI(self):
        # Scoreboard init
        self.setFixedWidth(300)
        self.setFixedHeight(778)
        self.setWindowTitle('ScoreBoard')
        self.setStyleSheet("""
            background-color: #f2f2f2;
            color: #333;
            font-family: Lucida Sans;
        """)

        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        # Create labels which will be updated by signals
        self.instructions = self.create_label("Instructions\n 1. Click anywhere to place"
                                              "\n a piece \n 2. Press ctrl+S or P to pass a turn \n 3. Press ctrl+r or R to reset the Game")
        self.player_turn = self.create_label(f"{self.player1_name}  ")
        self.timerLeft = self.create_label("Time remaining: ")
        self.label_playerStatus = self.create_label("Players Status")
        self.label_PrisonersBlack = self.create_label(f"{self.player1_name} Prisoners: ")
        self.label_PrisonersWhite = self.create_label(f"{self.player2_name} Prisoners: ")
        self.label_TerritoriesBlack = self.create_label(f"{self.player1_name} Territory: ")
        self.label_TerritoriesWhite = self.create_label(f"{self.player2_name} Territory: ")

        self.mainWidget.setLayout(self.mainLayout)
        self.add_widgets_to_layout()

        self.setWidget(self.mainWidget)

    def create_label(self, text):
        label = QLabel(text)
        label.setMargin(10)
        return label

    def add_widgets_to_layout(self):
        widgets = [self.instructions, self.player_turn, self.timerLeft, self.label_playerStatus,
                   self.label_PrisonersBlack, self.label_PrisonersWhite, self.label_TerritoriesBlack,
                   self.label_TerritoriesWhite]

        for widget in widgets:
            self.mainLayout.addWidget(widget)
            self.mainLayout.addSpacing(15)

    def make_connection(self, board):
        board.TO_TIME.connect(self.setTimeRemaining)
        board.captives.connect(self.updatePrisoners)
        board.territories.connect(self.updateTerritories)
        board.notifier.connect(self.displaynotification)
        board.player_turn.connect(self.updateturn)

    @pyqtSlot(int)
    def setTimeRemaining(self, timeRemainng):
        update = "Time Remaining:" + str(timeRemainng) + " sec"
        self.timerLeft.setText(update)

    def updateturn(self, player):
        if player == 1:
            self.player_turn.setText(f"Current Turn: {self.player1_name}")
        elif player == 2:
            self.player_turn.setText(f"Current Turn: {self.player2_name}")


    def updatePrisoners(self, n, Player):
        if Player == Piece.Black:
            update = f"{self.player1_name} Prisoners: " + n
            self.label_PrisonersBlack.setText(update)
        elif Player == Piece.White:
            update = f"{self.player2_name} prisoners: " + n
            self.label_PrisonersWhite.setText(update)

    def updateTerritories(self, n, Player):
        if Player == Piece.Black:
            update = f"{self.player1_name} territory: " + n
            self.label_TerritoriesBlack.setText(update)
        elif Player == Piece.White:
            update = f"{self.player2_name} territory: " + n
            self.label_TerritoriesWhite.setText(update)


    def displaynotification(self, message):
        dialog = QDialog(self)
        dialog.setFixedWidth(300)
        dialog.setWindowTitle("Notification")
        layout = QVBoxLayout()
        layout.addWidget(QLabel(message))
        dialog.setLayout(layout)
        dialog.exec()

# class ScoreBoard(QDockWidget):
#     BLACK_COLOR = QColor(Qt.GlobalColor.black).name()
#     WHITE_COLOR = QColor(Qt.GlobalColor.white).name()

#     def __init__(self):
#         super().__init__()
#         self.label_playerStatus = None
#         self.frm = None
#         self.label_TerritoriesBlack = None
#         self.label_TerritoriesWhite = None
#         self.label_PrisonersWhite = None
#         self.model = None
#         self.label_PrisonersBlack = None
#         self.timerLeft = None
#         self.player_turn = None
#         self.clicker = None
#         self.instructions = None
#         self.mainLayout = None
#         self.mainWidget = None
#         self.initUI()

#     def initUI(self):
#         # Score board init
#         self.resize(200, 200)
#         self.setFixedWidth(300)
#         self.setFixedHeight(778)
#         self.center()
#         self.setWindowTitle('ScoreBoard')
#         self.mainWidget = QWidget()
#         self.mainLayout = QVBoxLayout()

#         self.mainWidget.setStyleSheet(
#             """
#                  width: 100%; 
#                  padding:10px;
#                  text-align: center; 
#                  font-size: 12px;
#                  font-family:Lucida Sans;




#                } 
#                helpMenu
#             """
#         )

#         # create two labels which will be updated by signals
#         self.instructions = QLabel("Instructions\n 1. Click any where to place"
#                                    "\n a piece \n 2. Press ctrl+S or P to pass a turn \n 3. Press ctrl+r or R to reset the Game")

#         self.player_turn = QLabel("Current Turn: ")
#         self.timerLeft = QLabel("Time remaining: ")
#         self.label_playerStatus = QLabel("Players Status")
#         self.label_PrisonersBlack = QLabel("Black Prisoner: ")
#         self.label_PrisonersWhite = QLabel("White prisoners: ")
#         self.label_TerritoriesBlack = QLabel("Black Territory: ")
#         self.label_TerritoriesWhite = QLabel("Whites Territory: ")
#         col = QColor(Qt.GlobalColor.black)
#         self.frm = QFrame(self)
#         self.frm.setStyleSheet("QWidget { "
#                                "background-color: %s }"
#                                % col.name())
#         self.frm.setGeometry(20, 20, 100, 700)
#         self.mainWidget.setLayout(self.mainLayout)
#         self.mainLayout.addWidget(self.instructions)
#         self.mainLayout.addSpacing(70)
#         self.mainLayout.addWidget(self.player_turn)
#         self.mainLayout.addWidget(self.frm)
#         self.mainLayout.addSpacing(50)
#         self.mainLayout.addWidget(self.clicker)
#         self.mainLayout.addSpacing(70)
#         self.mainLayout.addWidget(self.timerLeft)
#         self.mainLayout.addSpacing(70)
#         self.mainLayout.addWidget(self.label_playerStatus)
#         self.mainLayout.addWidget(self.label_PrisonersBlack)
#         self.mainLayout.addWidget(self.label_PrisonersWhite)
#         self.mainLayout.addWidget(self.label_TerritoriesBlack)
#         self.mainLayout.addWidget(self.label_TerritoriesWhite)
#         # self.mainLayout.addSpacing(100)

#         self.setWidget(self.mainWidget)
#         self.show()

#     def center(self):
#         '''Just place in cneter'''

#     def make_connection(self, board):
#         '''this handles a signal sent from the board class'''
#         # when the updateTimerSignal is emitted in the board the setTimeRemaining slot receives it
#         board.TO_TIME.connect(self.setTimeRemaining)
#         # when the updatePrionersSignal is emitted in the board the updatePrisoners slot receives it
#         board.captives.connect(self.updatePrisoners)
#         board.territories.connect(self.updateTerritories)
#         board.notifier.connect(self.displaynotification)
#         board.player_turn.connect(self.updateturn)

#     @pyqtSlot(int)
#     def setTimeRemaining(self, timeRemainng):
#         '''updates the time remaining label to show the time remaining'''
#         update = "Time Remaining:" + str(timeRemainng) + " sec"
#         self.timerLeft.setText(update)

#     def updateturn(self, player):
#         if player == 1:
#             self.player_turn.setText("Current Turn: Black")
#             self.frm.setStyleSheet("QWidget { background-color: %s }" % self.BLACK_COLOR)
#         elif player == 2:
#             self.player_turn.setText("Current Turn: White")
#             self.frm.setStyleSheet("QWidget { background-color: %s }" % self.WHITE_COLOR)

#     def updatePrisoners(self, n, Player):
#         if Player == Piece.Black:
#             update = "Black Prisoners: " + n
#             self.label_PrisonersBlack.setText(update)

#         elif Player == Piece.White:
#             update = "White prisoners: " + n
#             self.label_PrisonersWhite.setText(update)

#     def updateTerritories(self, n, Player):
#         if Player == Piece.Black:
#             update = "Black territory: " + n
#             self.label_TerritoriesBlack.setText(update)

#         elif Player == Piece.White:
#             update = "White territory: " + n
#             self.label_TerritoriesWhite.setText(update)

#     def displaynotification(self, message):
#         dialog = QDialog(self)
#         dialog.setFixedWidth(300)
#         dialog.setWindowTitle("Notification")
#         layout = QVBoxLayout()
#         layout.addWidget(QLabel(message))
#         dialog.setLayout(layout)
#         dialog.exec()