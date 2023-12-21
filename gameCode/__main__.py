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
        # Set the background image
        self.setBackgroundImage("background.jpeg")
        self.create_main_layout()
        self.menu()


    def setBackgroundImage(self, image_path):
        # Create a QLabel to set the background image
        background_label = QLabel(self)
        background_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Load the image and set it as the background
        image = QImage(image_path)
        pixmap = QPixmap(image)
        background_label.setPixmap(pixmap)

        # Set the label as the central widget
        self.setCentralWidget(background_label)

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

    def menu(self):
        # set up menus
        mainMenu = self.menuBar()  # create and a menu bar
        # main menu stylesheet
        mainMenu.setStyleSheet(
            """
                 width: 100%; 
                 padding:10px;
                 padding-left:130px;
                 text-align: center; 
                 font-size: 15px;
                 font-family:Lucida Sans;
                 background: #f5f3f0;
                
               } 
               helpMenu
            """
        )

        # help menu
        helpAction = QAction("Help", self)
        helpAction.setShortcut("Ctrl+H")  # set shortcut
        helpMenu = mainMenu.addAction(helpAction)
        helpAction.triggered.connect(self.help)
        
        # About Menu
        aboutAction = QAction(QIcon("./icons/about.png"), "About", self)
        aboutAction.setShortcut("Ctrl+A")
        aboutMenu = mainMenu.addAction(aboutAction)  # connect the action to the function below
        aboutAction.triggered.connect(self.about)

        # help message display rules

    def help(self):
        msg = QMessageBox()
        msg.setText(
            "<p><strong>How to play go</strong></p> "
            "<p><strong>Rules: </strong></p>"
            "<p>A game of Go starts with an empty board. Each player has an effectively unlimited supply of pieces ("
            "called balls), one taking the black piece, the other taking white. The main object of the game is to "
            "use your pieces to form territories by surrounding vacant areas of the board. It is also possible to "
            "capture your opponent's pieces by completely surrounding them..</p> "

            "<p>Players take turns, placing one of their pieces on a vacant point at each turn, with Black playing "
            "first. Note that piece are placed on the intersections of the lines rather than in the squares and once "
            "played pieces are not moved. However they may be captured, in which case they are removed from the "
            "board, and kept by the capturing player as prisoners.</p> "

            "<br><strong> press ( Ctrl + E ) to Exit <br>"
            "<br><strong> press ( Ctrl + S ) to Skip Turn <br>"
            "<br><strong> press ( Ctrl + R ) or Reset <br>"

        )
        msg.setWindowTitle("Help")
        msg.exec()

    def about(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("About")
        msg.setText("ABOUT GO game")
        msg.setText("Go game v1.0\n\n@2022 ApexPlayground, SaheedCodes. All rights reserved")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GoGameHomePage()
    window.show()
    sys.exit(app.exec())