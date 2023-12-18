#board.py
import sys

from PyQt6 import QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class GoBoard(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()


        

    def initUI(self):
        self.button_size = 40  # Adjust the size of the buttons as needed
        self.current_color = 0  # 0 for black, 1 for white

        grid = QGridLayout()
        self.setLayout(grid)

        # Create a 7x7 grid of circular buttons for the Go board
        self.buttons = [[None] * 7 for _ in range(7)]
        for i in range(7):
            for j in range(7):
                button = QPushButton('')
                button.setFixedSize(self.button_size, self.button_size)
                button.setStyleSheet(f"QPushButton {{ border-radius: {self.button_size // 2}px; background-color: #BDBDBD; }}")
                grid.addWidget(button, i, j)
                button.clicked.connect(lambda _, i=i, j=j: self.on_button_click(i, j))
                self.buttons[i][j] = button

        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Go Board')
        self.show()

    def on_button_click(self, row, col):
        # Check if the button has been set
        if not self.buttons[row][col].isEnabled():
            return

        # Toggle color on each click
        self.current_color = 1 - self.current_color
        color = "#FFFFFF" if self.current_color else "#000000"

        # Update button color
        button = self.sender()
        button.setStyleSheet(f"QPushButton {{ border-radius: {self.button_size // 2}px; background-color: {color}; }}")
        button.setEnabled(False)  # Disable the button to prevent further clicks

        print(f'Stone placed at ({row}, {col}) with color {color}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    go_board = GoBoard()
    sys.exit(app.exec())
