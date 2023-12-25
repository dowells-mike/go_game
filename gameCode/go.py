# from PyQt6.QtWidgets import QDesktopWidget
from PyQt6 import QtCore
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from board import Board
from score_board import ScoreBoard


class Go(QMainWindow):
    def __init__(self):
        super().__init__()
        self.statusBar = None
        self.board = None
        self.scoreBoard = None
        self.initUI()

    def getBoard(self):
        return self.board

    def getScoreBoard(self):
        return self.scoreBoard

    def initUI(self):
        self.board = Board(self)
        self.setCentralWidget(self.board)
        self.board.setStyleSheet("padding: 0px;")
        self.scoreBoard = ScoreBoard()
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.scoreBoard)
        self.scoreBoard.make_connection(self.board)
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.resize(850, 850)
        self.setMinimumWidth(750)
        self.setMinimumHeight(650)
        self.center()
        self.setWindowTitle('Go')
        self.menu()
        self.show()

    def center(self):
        frameGeometry = self.frameGeometry()
        screen = QApplication.primaryScreen()
        centerPoint = screen.geometry().center()
        frameGeometry.moveCenter(centerPoint)
        self.move(frameGeometry.topLeft())


    def menu(self):
        mainMenu = self.menuBar()
        mainMenu.setStyleSheet(
            """
            width: 100%;
            padding: 10px;
            padding-left: 130px;
            text-align: center;
            font-size: 15px;
            font-family: Lucida Sans;
            background: #f5f3f0;
            """
        )

        skipAction = QAction("Skip Turn", self)
        skipAction.setShortcut("Ctrl+S")
        passMenu = mainMenu.addAction(skipAction)
        skipAction.triggered.connect(self.click)

        resetAction = QAction("Reset", self)
        resetAction.setShortcut("Ctrl+R")
        resetAction.triggered.connect(self.board.resetGame)
        resetMenu = mainMenu.addAction(resetAction)

        helpAction = QAction("Help", self)
        helpAction.setShortcut("Ctrl+H")
        helpMenu = mainMenu.addAction(helpAction)
        helpAction.triggered.connect(self.help)

        showWidgetAction = QAction("Show Widget", self)
        showWidgetAction.setShortcut("Ctrl+W")
        showwidgetMenu = mainMenu.addAction(showWidgetAction)
        showWidgetAction.triggered.connect(self.showScorerBoard)

        aboutAction = QAction(QIcon("./icons/about.png"), "About", self)
        aboutAction.setShortcut("Ctrl+A")
        aboutMenu = mainMenu.addAction(aboutAction)
        aboutAction.triggered.connect(self.about)

        exitAction = QAction("Exit", self)
        exitAction.setShortcut("Ctrl+E")
        exitMenu = mainMenu.addAction(exitAction)
        exitAction.triggered.connect(self.exit)

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

    def exit(self):
        QApplication.quit()

    def click(self):
        if self.getBoard().changeturn():  # link to board to change turn
            self.close()
        self.update()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_R:
            self.getBoard().resetGame()
            self.update()
        if event.key() == QtCore.Qt.Key.Key_P:
            if self.getBoard().skipTurn():
                self.close()
            self.update()

    def showScorerBoard(self):
        # Show or hide the scoreboard widget
        self.scoreBoard.setVisible(not self.scoreBoard.isVisible())
