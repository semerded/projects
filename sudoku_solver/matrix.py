import pygameaddons as app
import globals
import math

class Matrix:
    def __init__(self, matrixLength: int, matrixHeight: int) -> None:
        self.matrix = Matrix.makeEmptyMatrix(matrixLength, matrixHeight)
        self.sideMeasurement = 0
        self.matrixPosition = (0, 0)
        self.mouseGridpos = [0, 0]
        self.previousMouseGridPos = [0, 0]
        self.matrixRect = app.pygame.Rect(0, 0, 0, 0)
    # static
    def makeEmptyMatrix(length, height):
        matrix = []
        for i in range(height):
            matrixRow = []
            for j in range(length):
                matrixRow.append(0)
            matrix.append(matrixRow)
        return matrix
    
    def checkIfMatrix(possibleMatrix):
        isMatrix = True
        lenghtOfMatrixRow = len(possibleMatrix)
        if lenghtOfMatrixRow >= 2:
            for matrixColumn in range(lenghtOfMatrixRow):
                if len(matrixColumn) < 2:
                    isMatrix = False
        return isMatrix
     
    # instance               
    def _drawMatrixGrid(self):
        currentGridPosition = [0,0]
        
        for row in self.matrix:
            for column in row:
                gridUnitRect = app.pygame.Rect(self.matrixPosition[0] + self.gridUnitSide * currentGridPosition[0], self.matrixPosition[1] + self.gridUnitSide * currentGridPosition[1], self.gridUnitSide, self.gridUnitSide)
                currentGridPosition[0] += 1
                app.Drawing.border(1, gridUnitRect, app.Color.LIGHT_GRAY)
            currentGridPosition[1] += 1
            currentGridPosition[0] = 0
        self.matrixRect = app.pygame.Rect(self.matrixPosition[0], self.matrixPosition[1], self.gridUnitSide * self.getMatrixDimensions[0], self.gridUnitSide * self.getMatrixDimensions[1])
                
    def _drawMatrixItems(self):
        currentGridPosition = [0,0]
        for row in self.matrix:
            for column in row:
                if column != 0:
                    matrixUnitRect = app.pygame.Rect(self.matrixPosition[0] + self.gridUnitSide * currentGridPosition[0], self.matrixPosition[1] + self.gridUnitSide * currentGridPosition[1], self.gridUnitSide, self.gridUnitSide)
                    app.Drawing.rectangleFromRect(matrixUnitRect, globals.fieldColors[column])
                currentGridPosition[0] += 1
            currentGridPosition[1] += 1
            currentGridPosition[0] = 0
    
    def drawMatrix(self, position, sideMeasurement: int):
        self.matrixPosition = position
        
        self.sideMeasurement = sideMeasurement
        matrixWidth, matrixHeight = self.getMatrixDimensions # TODO! not reproducable
        self.gridUnitSide = self.sideMeasurement / matrixHeight
        self._drawMatrixItems()
        self._drawMatrixGrid()
        
    def checkForTouchInGrid(self) -> bool:
        if self.IsMatrixClicked():
            return self._findClickedGridUnit()
        else:
            self.previousMouseGridPos[0] = self.mouseGridpos[0]
            self.previousMouseGridPos[1] = self.mouseGridpos[1]
            return False
        
    def IsMatrixClicked(self):
        return app.Interactions.isHoldingInRect(self.matrixRect, app.mouseButton.leftMouseButton.value)
            
            
    def eraseMatrix(self):
        self.matrix = Matrix.makeEmptyMatrix(self.getMatrixDimensions[0], self.getMatrixDimensions[1])
        
    def setMatrix(self, newMatrix):
        self.matrix = newMatrix            
            
    def _findClickedGridUnit(self) -> bool: # return value for screen updating
        mousePos = app.pygame.mouse.get_pos()
        mousePos = (mousePos[0] - self.matrixPosition[0], mousePos[1] - self.matrixPosition[1])
        self.mouseGridpos[0] = math.ceil(mousePos[0] / self.gridUnitSide)
        self.mouseGridpos[1] = math.ceil(mousePos[1] / self.gridUnitSide)
        if self.mouseGridpos[0] != 0 and self.mouseGridpos[1] != 0:
            # To counter a strange bug where it would draw the bottom most square when you are drawing out of bounds above the screen
            if globals.colorPickerEnabled:
                self._pickColor()
                return True
            else:
                return self._updateMatrixWithClick()
        return False
    
    def _pickColor(self):
        globals.currentColor = self.matrix[self.mouseGridpos[1] - 1][self.mouseGridpos[0] - 1]
        
    def _updateMatrixWithClick(self):
        if self.mouseGridpos[0] != self.previousMouseGridPos[0] or self.mouseGridpos[1] != self.previousMouseGridPos[1]:
            self.matrix[self.mouseGridpos[1] - 1][self.mouseGridpos[0] - 1] = globals.currentColor
            self.drawMatrix(self.matrixPosition, self.sideMeasurement)
            self.previousMouseGridPos[0] = self.mouseGridpos[0]
            self.previousMouseGridPos[1] = self.mouseGridpos[1]
            return True
        return False
        
                
    @property
    def getMatrixDimensions(self):
        """
        returns the size of the matrix as tuple(size_Xaxis, size_Yaxis)
        """
        return len(self.matrix[0]), len(self.matrix)
    
    @property
    def getMatrix(self):
        return self.matrix
        