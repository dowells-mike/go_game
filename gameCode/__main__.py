import sys

from PyQt6 import QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from go import Go

class GoGameHomePage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GO GAME")
        self.setGeometry(600, 600, 600, 600)

        self.create_main_layout()

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

    def start_new_game(self):
        self.game_window = Go()
        self.game_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GoGameHomePage()
    window.show()
    sys.exit(app.exec())