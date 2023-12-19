# board.py
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout

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
<<<<<<< HEAD
        self.current_color = 1  # Set the initial color to black (0 for black, 1 for white)
=======
>>>>>>> 9e250eb940dded8e68f757bc2a856fe39f160820

    def initUI(self):
        self.button_size = 40  # Adjust the size of the buttons as needed

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

<<<<<<< HEAD
        print(f'Stone placed at ({row + 1}, {col + 1}) with color {color}')

        # Check if stones of the opposite color surround the newly placed stone
        self.check_captures(row, col)

    # Update the check_captures method
    # Update the check_captures method
    def check_captures(self, row, col):
        opposite_color = 1 - self.current_color
        opposite_color_str = "#FFFFFF" if opposite_color else "#000000"

        # Check neighboring stones of the opposite color
        neighbors = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1)
        ]

        # Check if at least one surrounding stone has the same color as the capturing player
        same_color_found = any(
            0 <= neighbor_row < 7
            and 0 <= neighbor_col < 7
            and self.buttons[neighbor_row][neighbor_col].styleSheet() == opposite_color_str
            for neighbor_row, neighbor_col in neighbors
        )

        if not same_color_found:
            captured_stones = []

            for neighbor_row, neighbor_col in neighbors:
                if 0 <= neighbor_row < 7 and 0 <= neighbor_col < 7:
                    neighbor_button = self.buttons[neighbor_row][neighbor_col]
                    if neighbor_button.isEnabled():
                        continue  # Skip empty intersections

                    # Check if the group of stones has no liberties
                    if not self.has_liberties(neighbor_row, neighbor_col):
                        captured_stones.append((neighbor_row, neighbor_col))

            # Remove captured stones from the board
            for captured_row, captured_col in captured_stones:
                captured_button = self.buttons[captured_row][captured_col]
                captured_button.setStyleSheet(f"QPushButton {{ border-radius: {self.button_size // 2}px; background-color: #BDBDBD; }}")
                captured_button.setEnabled(True)

                print(f'Stone at ({captured_row + 1}, {captured_col + 1}) captured by {self.current_color}')

    def has_liberties(self, row, col):
        # Check if a group of stones has liberties (empty neighboring intersections)
        neighbors = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1)
        ]

        for neighbor_row, neighbor_col in neighbors:
            if 0 <= neighbor_row < 7 and 0 <= neighbor_col < 7:
                neighbor_button = self.buttons[neighbor_row][neighbor_col]
                if neighbor_button.isEnabled():
                    return True  # At least one liberty found

        return False  # No liberties found

=======
        # Update game state
        self.update_game_state()

        print(f'Stone placed at ({row}, {col}) with color {color}')
>>>>>>> 9e250eb940dded8e68f757bc2a856fe39f160820

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


