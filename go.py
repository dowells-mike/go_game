#go.py
import sys

from PyQt6 import QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from board import GoBoard
from players import PlayerNameDialog

class GoGameHomePage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GO GAME")
        self.setGeometry(600, 600, 600, 600)

        self.create_main_layout()

        # set up menus
        Menu = self.menuBar()
        Menu.setNativeMenuBar(False)
        mainMenu = Menu.addMenu(" Main")
        helpMenu = Menu.addMenu(" Help")

        # Start New Game
        startAction = QAction("Start New Game", self)
        startAction.setShortcut("Ctrl+N")
        mainMenu.addAction(startAction)
        startAction.triggered.connect(self.start_new_game)

        # About
        aboutAction = QAction("About", self)
        aboutAction.setShortcut("Ctrl+I")
        helpMenu.addAction(aboutAction)
        aboutAction.triggered.connect(self.about)

        # Rules
        rulesAction = QAction("Rules", self)
        rulesAction.setShortcut("Ctrl+R")
        helpMenu.addAction(rulesAction)
        rulesAction.triggered.connect(self.show_rules)

    def create_main_layout(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Header
        header_label = QLabel("GO GAME", self)
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setFont(QFont('Times', 80, QFont.Weight.Bold))
        layout.addWidget(header_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Start Game Button
        start_game_button = QPushButton("Start Game", self)
        start_game_button.clicked.connect(self.start_new_game)
        start_game_button.setFixedSize(200, 60)
        layout.addWidget(start_game_button, alignment=Qt.AlignmentFlag.AlignCenter)

    # def start_new_game(self):
    #     dialog = PlayerNameDialog(self)
    #     if dialog.exec() == QDialog.DialogCode.Accepted:
    #         player1_name, player2_name = dialog.get_player_names()

    #         # Open a new window for the game with player names
    #         game_window = GoBoard()
    #         game_window.show()
    #         self.close()
    def start_new_game(self):
        dialog = PlayerNameDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            player1_name, player2_name = dialog.get_player_names()
        # Open a new window for the game with player names
        game_window = GoBoard(player1_name, player2_name)
        game_window.show()
        self.close()


    def about(self):
        about_text = (
            "GO GAME\n"
            "Version 1.0\n\n"
            "A simple Go Game application created with PyQt6."
        )
        QMessageBox.about(self, "About GO GAME", about_text)

    def show_rules(self):
        rules_text = (
            "GO GAME RULES\n\n"
            "1. Go is a two-player board game.\n"
            "2. Players take turns placing stones on the intersections of the board.\n"
            "3. Stones are captured by surrounding them with the opponent's stones.\n"
            "4. The player with the most territory at the end of the game wins.\n"
            "5. A player may pass their turn, and the game ends when both players pass.\n"
            "6. Ko rule prevents repeated board positions."
        )
        QMessageBox.about(self, "Rules of GO GAME", rules_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GoGameHomePage()
    window.show()
    sys.exit(app.exec())
