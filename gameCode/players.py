#players.py
import sys

from PyQt6 import QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class PlayerNameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Enter Player Names")

        # Set the size of the dialog
        self.resize(300, 200)  # Adjust the size as needed

        # If parent (main window) is provided, position the dialog at the center
        if parent:
            qr = self.frameGeometry()
            cp = parent.frameGeometry().center()
            qr.moveCenter(cp)
            self.move(qr.topLeft())
        else:
            self.setGeometry(300, 300, 400, 200)

        layout = QVBoxLayout(self)

        self.player1_label = QLabel("Player 1 Name:", self)
        self.player1_edit = QLineEdit(self)
        layout.addWidget(self.player1_label)
        layout.addWidget(self.player1_edit)

        self.player2_label = QLabel("Player 2 Name:", self)
        self.player2_edit = QLineEdit(self)
        layout.addWidget(self.player2_label)
        layout.addWidget(self.player2_edit)

        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)

    def get_player_names(self):
        return self.player1_edit.text(), self.player2_edit.text()