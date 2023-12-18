#board.py
import sys

from PyQt6 import QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class GoBoard(QMainWindow):
    def __init__(self, player1_name, player2_name):
        super().__init__()

        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_prisoners = 0
        self.player2_prisoners = 0
        self.player1_territory = 0
        self.player2_territory = 0
        self.initUI()

    def initUI(self):
        self.button_size = 40  # Adjust the size of the buttons as needed
        self.current_color = 0  # 0 for black, 1 for white

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # Create side widget
         # Create side widget
        side_widget = QDockWidget()  # Change QWidget to QDockWidget
        side_widget_contents = QWidget()  # Create a QWidget for the contents of the QDockWidget
        side_widget.setWidget(side_widget_contents)  # Set the QWidget as the contents of the QDockWidget
        side_widget_layout = QVBoxLayout()  # Create a QVBoxLayout
        side_widget_contents.setLayout(side_widget_layout)  # Set the QVBoxLayout to the QWidget
        side_widget.setStyleSheet("background-color: #d4d4d4;")  # Set a background color
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, side_widget)  # Add the QDockWidget to the QMainWindow


        side_widget_layout.setContentsMargins(10, 10, 10, 10)  # Add some margin
        side_widget_layout.setSpacing(10)  # Add some spacing between widgets
        instructions_label = QLabel("Game Instructions: \n1. Black starts first. \n2. Click on a grid to place a stone. \n3. Pass if you don't want to place a stone. \n4. Click reset to start a new game.")
        instructions_label.setStyleSheet("font-size: 14px; color: #333333;")  # Change font size and color
        side_widget_layout.addWidget(instructions_label)
        self.player1_label = QLabel(f"{self.player1_name}: 0 prisoners, 0 territory")
        self.player1_label.setStyleSheet("font-size: 16px; color: #333333;")  # Change font size and color
        self.player2_label = QLabel(f"{self.player2_name}: 0 prisoners, 0 territory")
        self.player2_label.setStyleSheet("font-size: 16px; color: #333333;")  # Change font size and color
        self.turn_label = QLabel(f"{self.player1_name}'s turn")
        self.turn_label.setStyleSheet("font-size: 18px; color: #000000;")  # Change font size and color
        pass_button = QPushButton("Pass")
        pass_button.setStyleSheet("font-size: 16px;")  # Change font size
        pass_button.clicked.connect(self.pass_turn)
        reset_button = QPushButton("Reset")
        reset_button.setStyleSheet("font-size: 16px;")  # Change font size
        reset_button.clicked.connect(self.reset_game)

        side_widget_layout.addWidget(self.player1_label)
        side_widget_layout.addWidget(self.player2_label)
        side_widget_layout.addWidget(self.turn_label)
        side_widget_layout.addWidget(pass_button)
        side_widget_layout.addWidget(reset_button)


         # Create Go board
        central_widget = QWidget()  # Create a QWidget for the central widget
        self.setCentralWidget(central_widget)  # Set the QWidget as the central widget
        main_layout = QHBoxLayout()  # Create a QHBoxLayout
        central_widget.setLayout(main_layout)  # Set the QHBoxLayout to the QWidget
        grid = QGridLayout()  # Create a QGridLayout
        main_layout.addLayout(grid)  # Add the QGridLayout to the QHBoxLayout


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
        color = "#FFFFFF"if self.current_color else "#000000"

        # Update button color
        button = self.sender()
        button.setStyleSheet(f"QPushButton {{ border-radius: {self.button_size // 2}px; background-color: {color}; }}")
        button.setEnabled(False)  # Disable the button to prevent further clicks

        # Update game state
        self.update_game_state()

        print(f'Stone placed at ({row}, {col}) with color {color}')

    def update_game_state(self):
        # This is where you would update the number of prisoners and territory for each player
        # For now, we'll just increment these values each turn
        if self.current_color == 0:
            self.player1_prisoners += 1
            self.player1_territory += 1
        else:
            self.player2_prisoners += 1
            self.player2_territory += 1

        # Update labels
        self.player1_label.setText(f"{self.player1_name}: {self.player1_prisoners} prisoners, {self.player1_territory} territory")
        self.player2_label.setText(f"{self.player2_name}: {self.player2_prisoners} prisoners, {self.player2_territory} territory")
        self.turn_label.setText(f"{self.player1_name if self.current_color == 0 else self.player2_name}'s turn")

    def pass_turn(self):
        # Switch turns without placing a stone
        self.current_color = 1 - self.current_color
        self.turn_label.setText(f"{self.player1_name if self.current_color == 0 else self.player2_name}'s turn")

    def reset_game(self):
        # Reset game state
        self.player1_prisoners = 0
        self.player2_prisoners = 0
        self.player1_territory = 0
        self.player2_territory = 0
        self.current_color = 0

        # Reset labels
        self.player1_label.setText(f"{self.player1_name}: 0 prisoners, 0 territory")
        self.player2_label.setText(f"{self.player2_name}: 0 prisoners, 0 territory")
        self.turn_label.setText(f"{self.player1_name}'s turn")

        # Enable all buttons and reset their color
        for row in self.buttons:
            for button in row:
                button.setEnabled(True)
                button.setStyleSheet(f"QPushButton {{ border-radius: {self.button_size // 2}px; background-color: #BDBDBD; }}")


