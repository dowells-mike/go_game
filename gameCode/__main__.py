import sys
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from go import Go

class GoGameHomePage(QMainWindow):
    BACKGROUND_IMAGE = "background.jpeg"
    SHORTCUT_EXIT = "Ctrl+E"
    SHORTCUT_SKIP_TURN = "Ctrl+S"
    SHORTCUT_RESET = "Ctrl+R"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("GO GAME")
        self.setGeometry(600, 600, 600, 600)
        self.setBackgroundImage(self.BACKGROUND_IMAGE)
        self.create_main_layout()
        self.menu()

    def setBackgroundImage(self, image_path):
        background_label = QLabel(self)
        background_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image = QImage(image_path)
        pixmap = QPixmap(image)
        background_label.setPixmap(pixmap)
        self.setCentralWidget(background_label)

    def create_main_layout(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        header_label = QLabel("GO GAME", self)
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setFont(QFont('Times', 80, QFont.Weight.Bold))
        layout.addWidget(header_label, alignment=Qt.AlignmentFlag.AlignCenter)

        start_game_button = QPushButton("Start Game", self)
        start_game_button.clicked.connect(self.start_new_game)
        start_game_button.setFixedSize(200, 60)
        layout.addWidget(start_game_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def start_new_game(self):
        self.game_window = Go()
        self.game_window.show()
        self.close()

    def menu(self):
        mainMenu = self.menuBar()
        mainMenu.setStyleSheet(
        """
        QMenuBar {
            width: 100%; 
            padding:10px;
            padding-left:130px;
            text-align: center; 
            font-size: 15px;
            font-family:Lucida Sans;
            background: #f5f3f0;
        }
        """
    )


        helpAction = QAction("Help", self)
        helpAction.setShortcut(self.SHORTCUT_SKIP_TURN)
        helpMenu = mainMenu.addAction(helpAction)
        helpAction.triggered.connect(self.help)

        aboutAction = QAction(QIcon("./icons/about.png"), "About", self)
        aboutAction.setShortcut(self.SHORTCUT_RESET)
        aboutMenu = mainMenu.addAction(aboutAction)
        aboutAction.triggered.connect(self.about)

    def load_style_sheet(self, file_path):
        with open(file_path, 'r') as file:
            return file.read()

    def help(self):
        help_text = """
            <p><strong>How to play Go</strong></p>
            <p><strong>Rules:</strong></p>
            <p>Go is played on a board with an empty grid. Players, one with black pieces and the other with white pieces,
            take turns placing their pieces on vacant intersections. The goal is to form territories by surrounding empty areas
            and capturing opponent's pieces by surrounding them.</p>

            <p>Pieces are placed on intersections, not in squares. Once played, pieces are not moved, but they can be captured,
            in which case they are removed and kept as prisoners by the capturing player.</p>

            <br><strong>Press (Ctrl + E) to Exit</strong>
            <br><strong>Press (Ctrl + S) to Skip Turn</strong>
            <br><strong>Press (Ctrl + R) to Reset</strong>
        """

        msg = QMessageBox()
        msg.setText(help_text)
        msg.setWindowTitle("Help")
        msg.exec()

    def about(self):
        about_text = """
            <p><strong>About GO Game</strong></p>
            <p>Version: 1.0.0</p>
            <p>&copy; 2023 Mike, Segun, Kehinde. All rights reserved.</p>

            <p>GO Game is a classic board game where players compete to control territories by strategically placing pieces on
            the board. This version brings you a digital adaptation for a challenging and enjoyable gaming experience.</p>

            <br><strong>Press OK to continue</strong>
        """

        msg = QMessageBox(self)
        msg.setWindowTitle("About GO Game")
        msg.setText(about_text)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GoGameHomePage()
    window.show()
    sys.exit(app.exec())