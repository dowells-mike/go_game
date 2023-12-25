# Import necessary classes from other modules
from piece import Piece
from balls import Balls

# Define the GameLogic class
class GameLogic:
    # Initialize class-level variables
    turn = Piece.White
    xPosition = 0
    yPosition = 0
    boardArray = 0
    captiveIsWhite = 0
    captiveIsBlack = 0
    territoriesIsWhite = 0
    territoriesIsBlack = 0

    # Method to update current parameters
    def updateparams(self, boardArray, xPosition, yPosition):
        # Update current variables with provided values
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.boardArray = boardArray

    # Method to check game logic based on the current state
    def checklogic(self, boardArray, xpos, ypos):
        # Update current variables with provided values
        self.xPosition = xpos
        self.yPosition = ypos
        self.boardArray = boardArray

    # Method to check if the position is not occupied
    def postionNotOccupied(self):
        # Assert that the insertion position is not occupied
        if self.boardArray[self.yPosition][self.xPosition].Piece == Piece.NoPiece:
            return True
        else:
            return False

    # Method to toggle turns between players
    def toggleTurns(self):
        # Swap turns between black and white
        print("turn changed")
        if self.turn == Piece.Black:
            self.turn = Piece.White
        else:
            self.turn = Piece.Black

    # Method to place a piece on the board
    def plotTheBalls(self):
        # Place a piece on the selected position based on the current turn
        if self.turn == Piece.Black:
            self.boardArray[self.yPosition][self.xPosition].Piece = Piece.Black
        else:
            self.boardArray[self.yPosition][self.xPosition].Piece = Piece.White

        # Print information about the placed piece
        print("Liberties = " + str(self.boardArray[self.yPosition][self.xPosition].liberties) + "x pos = " + str(
            self.boardArray[self.yPosition][self.xPosition].x) + "y pos = " + str(self.boardArray[self.yPosition][self.xPosition].y))

    # Method to update liberties of all available pieces on the board
    def updateLiberty(self):
        # Iterate through the board and update liberties for each piece
        count = 0
        for row in self.boardArray:
            for cell in row:
                count = 0
                if cell.Piece != Piece.NoPiece:
                    pieceColor = cell.Piece

                    # Check liberties in each direction and update count
                    if cell.getTop(self.boardArray) is not None and (
                            cell.getTop(self.boardArray).Piece == pieceColor or cell.getTop(
                        self.boardArray).Piece == Piece.NoPiece):
                        count = count + 1
                    if cell.getRight(self.boardArray) is not None and (
                            cell.getRight(self.boardArray).Piece == pieceColor or cell.getRight(
                        self.boardArray).Piece == Piece.NoPiece):
                        count = count + 1
                    if cell.getLeft(self.boardArray) is not None and (
                            cell.getLeft(self.boardArray).Piece == pieceColor or cell.getLeft(
                        self.boardArray).Piece == Piece.NoPiece):
                        count = count + 1
                    if cell.getDown(self.boardArray) is not None and (
                            cell.getDown(self.boardArray).Piece == pieceColor or cell.getDown(
                        self.boardArray).Piece == Piece.NoPiece):
                        count = count + 1
                    # Set the liberties count for the current cell
                    cell.setLiberties(count)

    # Method to update captives on the board
    def updateCaptives(self):
        # Remove all pieces with 0 liberties left
        for row in self.boardArray:
            for cell in row:
                if cell.liberties == 0 and cell.Piece != Piece.NoPiece:
                    if cell.Piece == Piece.Black:
                        self.captiveIsWhite = self.captiveIsWhite + 1
                        self.boardArray[cell.y][cell.x] = Balls(Piece.NoPiece, cell.x, cell.y)
                        print("Black Ball Captured at x: " + str(cell.x) + ", y: " + str(cell.y))
                        return "Black Ball Captured at x: " + str(cell.x) + ", y: " + str(cell.y)
                    elif cell.Piece == Piece.White:
                        self.captiveIsBlack = self.captiveIsBlack + 1
                        self.boardArray[cell.y][cell.x] = Balls(Piece.NoPiece, cell.x, cell.y)
                        print("White Ball Captured at x: " + str(cell.x) + ", y: " + str(cell.y))
                        return "White Ball Captured at x: " + str(cell.x) + ", y: " + str(cell.y)

    # Method to update captives in a specific situation
    def updateCaptivesTheSecond(self):
        # Check neighboring cells and capture pieces if necessary
        if self.boardArray[self.yPosition][self.xPosition].getTop(self.boardArray) is not None and self.boardArray[self.yPosition][
            self.xPosition].getTop(self.boardArray).liberties == 0 and self.boardArray[self.yPosition][
            self.xPosition].getTop(self.boardArray).Piece != Piece.NoPiece:
            return self.capturePiece(self.xPosition, self.yPosition - 1)
        elif self.boardArray[self.yPosition][self.xPosition].getRight(self.boardArray) is not None and self.boardArray[self.yPosition][
            self.xPosition].getRight(self.boardArray).liberties == 0 and self.boardArray[self.yPosition][
            self.xPosition].getRight(self.boardArray).Piece != Piece.NoPiece:
            return self.capturePiece(self.xPosition + 1, self.yPosition)
        elif self.boardArray[self.yPosition][self.xPosition].getLeft(self.boardArray) is not None and self.boardArray[self.yPosition][
            self.xPosition].getLeft(self.boardArray).liberties == 0 and self.boardArray[self.yPosition][
            self.xPosition].getLeft(self.boardArray).Piece != Piece.NoPiece:
            return self.capturePiece(self.xPosition - 1, self.yPosition)
        elif self.boardArray[self.yPosition][self.xPosition].getDown(self.boardArray) is not None and self.boardArray[self.yPosition][
            self.xPosition].getDown(self.boardArray).liberties == 0 and self.boardArray[self.yPosition][
            self.xPosition].getDown(self.boardArray).Piece != Piece.NoPiece:
            return self.capturePiece(self.xPosition, self.yPosition + 1)

    # Method to capture a piece at a specific position
    def capturePiece(self, xpos, ypos):
        # Capture a piece at the given position
        if self.boardArray[ypos][xpos].Piece == 1:  # if the piece is white
            self.captiveIsBlack = self.captiveIsBlack + 1
            self.boardArray[ypos][xpos] = Balls(Piece.NoPiece, xpos, ypos)
            return "White piece Captured at x: " + str(xpos) + ", y: " + str(ypos)
        else:  # if the piece is black
            self.captiveIsWhite = self.captiveIsWhite + 1
            self.boardArray[ypos][xpos] = Balls(Piece.NoPiece, xpos, ypos)
            return "Black piece Captured at x: " + str(xpos) + ", y: " + str(ypos)

    # Method to check if a move is considered bad
    def isBadMove(self):
        oppositeplayer = 0
        if self.turn == Piece.Black:
            oppositeplayer = Piece.White
        else:
            oppositeplayer = Piece.Black
        count = 0

        # Check adjacent cells and count how many belong to the opposite player
        if self.boardArray[self.yPosition][self.xPosition].getTop(self.boardArray) is None or self.boardArray[self.yPosition][
            self.xPosition].getTop(self.boardArray).Piece == oppositeplayer:
            count = count + 1
        if self.boardArray[self.yPosition][self.xPosition].getLeft(self.boardArray) is None or self.boardArray[self.yPosition][
            self.xPosition].getLeft(self.boardArray).Piece == oppositeplayer:
            count = count + 1
        if self.boardArray[self.yPosition][self.xPosition].getRight(self.boardArray) is None or self.boardArray[self.yPosition][
            self.xPosition].getRight(self.boardArray).Piece == oppositeplayer:
            count = count + 1
        if self.boardArray[self.yPosition][self.xPosition].getDown(self.boardArray) is None or self.boardArray[self.yPosition][
            self.xPosition].getDown(self.boardArray).Piece == oppositeplayer:
            count = count + 1

        # Check if the move is considered bad based on the surrounding conditions
        if count == 4:
            if self.boardArray[self.yPosition][self.xPosition].getTop(self.boardArray) is not None and self.boardArray[self.yPosition][
                self.xPosition].getTop(self.boardArray).liberties == 1:
                return False
            if self.boardArray[self.yPosition][self.xPosition].getLeft(self.boardArray) is not None and \
                    self.boardArray[self.yPosition][
                        self.xPosition].getLeft(self.boardArray).liberties == 1:
                return False
            if self.boardArray[self.yPosition][self.xPosition].getRight(self.boardArray) is not None and \
                    self.boardArray[self.yPosition][
                        self.xPosition].getRight(self.boardArray).liberties == 1:
                return False
            if self.boardArray[self.yPosition][self.xPosition].getDown(self.boardArray) is not None and \
                    self.boardArray[self.yPosition][
                        self.xPosition].getDown(self.boardArray).liberties == 1:
                return False
            return True
        else:
            return False

    # Methods to retrieve information about prisoners, territories, and scores
    def getBlackPrisoner(self):
        return str(self.captiveIsBlack)

    def getWhitePrisoner(self):
        return str(self.captiveIsWhite)

    def getBlackTerritories(self):
        return str(self.territoriesIsBlack)

    def getWhiteTerritories(self):
        return str(self.territoriesIsWhite)

    # Method to update territories based on the current state of the board
    def updateTeritories(self):
        # Count the number of positions occupied by each player
        counterOne = 0
        countTwo = 0
        for row in self.boardArray:
            for cell in row:
                if cell.Piece == Piece.Black:
                    counterOne = counterOne + 1
                elif cell.Piece == Piece.White:
                    countTwo = countTwo + 1
        # Update the territories for both players
        self.territoriesIsWhite = countTwo
        self.territoriesIsBlack = counterOne

    # Method to return scores for a specific player
    def returnTheScores(self, Piece):
        if Piece == 2:
            return self.territoriesIsBlack + self.captiveIsBlack
        else:
            return self.territoriesIsWhite + self.captiveIsWhite
