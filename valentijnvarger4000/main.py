from colors import Color
from fonts import Font
from os import environ
from random import randint
from time import sleep
import keyboard

environ['SDL_VIDEO_CENTERED'] = '1'

import pygameaddons as app

APP = app.AppConstructor(app.ScreenUnit.dw(100), app.ScreenUnit.dh(100), app.pygame.NOFRAME)


loadingScreen = app.Image("images/loadingScreen.jpg")
loadingScreen.resize(app.ScreenUnit.vw(100), app.ScreenUnit.vh(100))

# bluescreen setup
image = app.Image("images/bluescreen.png")
image.resize(app.ScreenUnit.vw(100), app.ScreenUnit.vh(100))
clock = app.pygame.time.Clock()
counterTextFont = app.pygame.font.SysFont("Segoe UI", 36)

# end
thumbUp = app.Image("images/thumbup.png")
thumbUp.resize(app.ScreenUnit.vw(100), app.ScreenUnit.vh(100))

counter = 0

questionText = app.Text(Font.FONT150, Color.WHITE)
yesButton = app.Button((app.ScreenUnit.vw(20), app.ScreenUnit.vh(10)), Color.GREEN)
yesButton.text("JAAAA!!!", Font.FONT50, Color.WHITE)
noButton = app.Button((app.ScreenUnit.vw(20), app.ScreenUnit.vh(10)), Color.RED)
noButton.text("NEEEE!!!", Font.FONT50, Color.WHITE)

noButtonPosition = (app.ScreenUnit.vw(15), app.ScreenUnit.vh(75))


loadingScreen.place(0, 0)
APP.updateDisplay()
sleep(4)


# choice button
while True:
    APP.eventHandler(app.pygame.event.get())
    APP.maindisplay.fill(Color.BLACK)

    questionText.centerTextInScreen("Wil je mijn valentijn zijn?")
    noButton.place(*noButtonPosition)
    if noButton.onMouseClick():
        while True:
            noButtonPosition = (app.ScreenUnit.vw(randint(0, 90)), app.ScreenUnit.vh(randint(0, 90)))
            noButton.place(*noButtonPosition)
            
            if not noButton.inRect(yesButton.getRect):
                break

    yesButton.place(app.ScreenUnit.vw(65), app.ScreenUnit.vh(75))
    if yesButton.onMouseClick():
        break

sleep(0.5)
# bluescreen
app.pygame.mouse.set_visible(False)

sleep(0.5)

while True:
    APP.eventHandler(app.pygame.event.get())
    APP.maindisplay.fill((0, 120, 215))
    
    keyboard.block_key("alt")
    keyboard.block_key("tab")
    keyboard.block_key("delete")
    keyboard.block_key("control")
    keyboard.block_key("Win")

    if counter == 100:
        sleep(1)
        break

    if randint(0, 200) == 69:
        if counter == 100:
            break
        counter += randint(3, 20)
    if counter > 100:
        counter = 100

    image.place(0, 0)
    app.Drawing.rectangle(
        0, APP.getdisplayDimensions[1] * 0.565, APP.getdisplayDimensions[0], 40, (0, 120, 215))
    app.Text.simpleText((165, APP.getdisplayDimensions[1] * 0.555), f"{counter}% complete", counterTextFont, Color.WHITE, False)

while True:
    APP.eventHandler(app.pygame.event.get())
    
    thumbUp.place(0, 0)
    
    if APP.keyboardClick(app.pygame.K_RETURN):
        break
    
    

