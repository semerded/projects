import pygameaddons as app
from matrix import Matrix

APP = app.AppConstructor(app.ScreenUnit.dh(85), app.ScreenUnit.dh(95), manualUpdating=True)

SUDOKU_GRID = Matrix(9, 9)

startSolveButton = app.Button((app.ScreenUnit.dh(40), app.ScreenUnit.dh(8)), app.Color.GREEN)
# eraseSudoku = app.Button()




while True:
    APP.maindisplay.fill(app.Color.WHITE)
    APP.eventHandler(app.pygame.event.get())
    
    SUDOKU_GRID.checkForTouchInGrid()
    SUDOKU_GRID.drawMatrix((0, 0), app.ScreenUnit.dh(85))
    
    startSolveButton.place(app.ScreenUnit.dh(2.5), app.ScreenUnit.dh(86))
    
    APP.updateDisplay()
    