# board.py
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout

class GoBoard(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.current_color = 1  # Set the initial color to black (0 for black, 1 for white)

    def initUI(self):
        self.button_size = 40  # Adjust the size of the buttons as needed

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    go_board = GoBoard()
    sys.exit(app.exec())
