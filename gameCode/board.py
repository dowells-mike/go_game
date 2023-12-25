from collections import namedtuple
from copy import copy
from PyQt6.QtWidgets import QFrame, QStatusBar, QMessageBox
from PyQt6.QtCore import Qt, QBasicTimer, pyqtSignal, QPoint
from PyQt6.QtGui import QPainter, QBrush, QColor
from piece import Piece
from balls import Balls
from game_logic import GameLogic
from PyQt6.QtCore import QCoreApplication

class Board(QFrame):
    boardWidth = 7  # board width
    boardHeight = 7  # board height
    timerSpeed = 1000  # timer set to 1 sec
    counter = 60  # countdown
    gamelogic = GameLogic()  # getting game logic class
    passcount = 0
    listenToTime = pyqtSignal(int)
    listenToClick = pyqtSignal(str)
    captives = pyqtSignal(str, int)
    territories = pyqtSignal(str, int)
    notifier = pyqtSignal(str)
    playerTurn = pyqtSignal(int)

    def __init__(self, parent):
        super().__init__(parent)
        self.boardArray = None
        self.isStarted = None
        self.timer = None
        self.initBoard()
        self.__gameState__ = []  # List to store the state of the game

    def initBoard(self):
        # Initialize the game board
        self.timer = QBasicTimer()
        self.isStarted = False
        self.start()
        self.boardArray = [[Balls(Piece.NoPiece, i, j) for i in range(self.boardWidth)] for j in range(self.boardHeight)]
        self.gamelogic = GameLogic()
        self.printBoardArray()

    def printBoardArray(self):
        # Print the boardArray for debugging
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

    def squareWidth(self):
        return self.contentsRect().width() / self.boardWidth

    def squareHeight(self):
        return self.contentsRect().height() / self.boardHeight

    def start(self):
        # Start the game
        self.isStarted = True
        self.resetGame()
        self.timer.start(self.timerSpeed, self)
        print("start () - timer is started")

    def timerEvent(self, event):
        # Handle timer events
        if event.timerId() == self.timer.timerId():
            if self.counter == 0:
                self.gameOver()
            else:
                self.counter -= 1
                self.listenToTime.emit(self.counter)
        else:
            super(Board, self).timerEvent(event)

    def paintEvent(self, event):
        # Paint the board and pieces
        painter = QPainter(self)
        self.drawBoardSquares(painter)
        self.drawPieces(painter)

    def mousePressEvent(self, event):
        # Handle mouse click events
        clickLoc = f"click location [{event.position().x()},{event.position().y()}]"
        print(f"mousePressEvent() - {clickLoc}")
        self.mousePosToColRow(event)
        self.listenToClick.emit(clickLoc)

    def mousePosToColRow(self, event):
        # Convert mouse click event to row and column
        xPosition, yPosition = event.position().x(), event.position().y()
        xCoordinate, yCoordinate = xPosition / self.squareWidth(), yPosition / self.squareHeight()
        x, y = round(xCoordinate) - 1, round(yCoordinate) - 1
        self.gamelogic.updateparams(self.boardArray, x, y)
        if self.canWePlaceBallAtChosenPosition():
            self.placeBall()
            self.updateTerritoriesAndCaptives()
        self.update()

    def drawBoardSquares(self, painter):
        # Draw the board squares
        color = QColor(169, 169, 169)
        color2 = QColor(211, 211, 211)
        brush = QBrush(Qt.BrushStyle.SolidPattern)
        brush.setColor(color)
        for row in range(0, self.boardHeight):
            for col in range(0, self.boardWidth):
                painter.save()
                colTransformation, rowTransformation = self.squareWidth() * col, self.squareHeight() * row
                painter.translate(colTransformation, rowTransformation)
                painter.fillRect(col, row, round(self.squareWidth()), round(self.squareHeight()), brush)
                painter.restore()
                brush.setColor(color2 if brush.color() == color else color)

    def drawPieces(self, painter):
        # Draw the game pieces
        for row in range(len(self.boardArray)):
            for col in range(len(self.boardArray[0])):
                painter.save()
                painter.translate((self.squareWidth() * row) + self.squareWidth() * 0.70,
                                  (self.squareHeight() * col) + self.squareHeight() * 0.70)
                color = self.getPieceColor(row, col)
                painter.setPen(color)
                painter.setBrush(color)
                radius = self.squareWidth() / 3
                center = QPoint(round(radius), round(radius))
                painter.drawEllipse(center, round(radius), round(radius))
                painter.restore()

    def getPieceColor(self, row, col):
        # Get the color of the piece at the specified row and column
        piece = self.boardArray[col][row].Piece
        if piece == Piece.NoPiece:
            return QColor(Qt.GlobalColor.transparent)
        elif piece == Piece.White:
            return QColor(Qt.GlobalColor.white)
        elif piece == Piece.Black:
            return QColor(Qt.GlobalColor.black)

    def canWePlaceBallAtChosenPosition(self):
        # Check if it's safe to place a ball at the chosen position
        if self.gamelogic.postionNotOccupied():
            if self.gamelogic.isBadMove():
                self.notifyUser("Move not Allowed")
                return False
            return True
        else:
            self.notifyUser("Spot Occupied")
            return False

    def placeBall(self):
        # Place the ball on the board
        self.gamelogic.plotTheBalls()
        self.gamelogic.updateLiberty()
        message = self.gamelogic.updateCaptivesTheSecond()
        if message is not None:
            self.notifyUser(message)
            print("Stone captured")
            self.gamelogic.updateLiberty()
        self.gamelogic.updateTeritories()
        self.__addCurrentStateToGlobalState__()
        if not self._check_for_ko():
            self.passcount = 0
            self.changeturn()
        else:
            self.handleKo()

    def __addCurrentStateToGlobalState__(self):
        # Add the current board state to the state array
        self.__gameState__.append(self.copyThisBoard())
        self.printRecentStates()

    def printRecentStates(self):
        # Print recent states for debugging
        try:
            print("Last move")
            print('\n'.join(['\t'.join([str(cell.Piece) for cell in row]) for row in self.__gameState__[-1]]))
            print("Second Last")
            print('\n'.join(['\t'.join([str(cell.Piece) for cell in row]) for row in self.__gameState__[-2]]))
            print("3rd Last")
            print('\n'.join(['\t'.join([str(cell.Piece) for cell in row]) for row in self.__gameState__[-3]]))
        except IndexError:
            return None

    def __removeFromGlobalState__(self, previousstate):
        # Remove and load game state from history
        print("Removed from global state stack")
        for rowIndex, row in enumerate(previousstate):
            for colIndex, cell in enumerate(row):
                self.boardArray[rowIndex][colIndex] = Balls(cell.Piece, colIndex, rowIndex)
        self.printBoardArray()

    def copyThisBoard(self):
        # Copy the current state of the board
        return [[Balls(cell.Piece, i, j) for i, cell in enumerate(row)] for j, row in enumerate(self.boardArray)]

    def _check_for_ko(self):
        # Check for KO
        try:
            if self.assertBoardsAreEqual(self.__gameState__[-1], self.__gameState__[-3]):
                self.notifyUser('KO. Revert back now')
                return True
        except IndexError:
            pass
        return False

    def assertBoardsAreEqual(self, current, previous):
        # Check for equality of two boards
        return all(cell.Piece == current[row][col].Piece for row, row_cells in enumerate(previous) for col, cell in enumerate(row_cells))

    def changeturn(self):
        # Change the turn to the next player and update the interface
        self.gamelogic.toggleTurns()
        self.counter = 60
        self.playerTurn.emit(self.gamelogic.turn)

    def updateTerritoriesAndCaptives(self):
        # Emit signals for territories and captives
        self.captives.emit(self.gamelogic.getBlackPrisoner(), Piece.Black)
        self.captives.emit(str(self.gamelogic.getWhitePrisoner()), Piece.White)
        self.territories.emit(str(self.gamelogic.getWhiteTerritories()), Piece.White)
        self.territories.emit(str(self.gamelogic.getBlackTerritories()), Piece.Black)

    def whoIsTheWinner(self):
        # Compare both players' scores and determine the winner
        blackscore, whitescore = self.gamelogic.returnTheScores(Piece.Black), self.gamelogic.returnTheScores(Piece.White)
        self.notifyUser(f"Scores : \n Black : {blackscore}\n White : {whitescore}")
        if blackscore > whitescore:
            self.notifyUser("Black Wins")
        elif blackscore < whitescore:
            self.notifyUser("White Wins")
        else:
            self.notifyUser("Game is a Draw")

    def getScore(self, Piece):
        return self.gamelogic.returnTheScores(Piece)

    def notifyUser(self, message):
        self.notifier.emit(message)

    def resetGame(self):
        # Reset the game state
        print("Game Reset")
        self.notifyUser("Game Reset")
        self.boardArray = [[Balls(Piece.NoPiece, i, j) for i in range(self.boardWidth)] for j in range(self.boardHeight)]
        self.gamelogic.blackprisoners = 0
        self.gamelogic.whiteprisoners = 0
        self.gamelogic.blackterritories = 0
        self.gamelogic.whiteterritories = 0
        self.gamelogic.turn = Piece.Black
        self.timer.stop()
        self.counter = 60
        self.timer.start(self.timerSpeed, self)

    def skipTurn(self):
        # Skip a turn and check for game over conditions
        self.notifyUser("Move Passed")
        self.passcount += 1
        self.gamelogic.toggleTurns()
        if self.passcount == 2:
            self.notifyUser("Double turn skipped, game over")
            self.whoIsTheWinner()
            return True
        return False

    def gameOver(self):
        # Handle game over conditions
        self.notifyUser("Timer Ran out : Game over")
        winner = "White Player Wins" if self.gamelogic.turn == Piece.Black else "Black Player Wins"
        self.notifyUser(winner)
        reply = QMessageBox.question(self, 'Game Over', f"{winner}\nDo you want to play a new game?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.resetGame()
        else:
            QCoreApplication.instance().quit()

    def handleKo(self):
        # Handle KO situation
        if self.gamelogic.turn == Piece.White:
            self.gamelogic.captiveIsWhite -= 1
        else:
            self.gamelogic.captiveIsBlack -= 1
        self.__removeFromGlobalState__(self.__gameState__[-2])
        self.gamelogic.updateLiberty()
        self.gamelogic.updateTeritories()
        self.__addCurrentStateToGlobalState__()