import pygameaddons as app
from matrix import Matrix

APP = app.AppConstructor(app.ScreenUnit.dh(90), app.ScreenUnit.dh(90), manualUpdating=True)
APP.setAspectratio(app.ScreenUnit.aspectRatio(app.aspectRatios.ratio1to1), height=app.ScreenUnit.dh(90))

SUDOKU_GRID = Matrix(9, 9)