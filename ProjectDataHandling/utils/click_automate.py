

import pyautogui

def click_button_from_picture(img_path, clicks=True, confidence=0.8):
    # click on a button when we have a picture of the button
    # the button must be visible when the code runs

    button7location = pyautogui.locateCenterOnScreen(img_path, 
                                                     grayscale=False, 
                                                     confidence=confidence)
    
    if clicks:
        pyautogui.click(button7location)
    
    return button7location


def return_mouse_pos__screen_size(printer=False):
    
    screenWidth, screenHeight = pyautogui.size() 
    # Get the size of the primary monitor.
    currentMouseX, currentMouseY = pyautogui.position() 
    # Get the XY position of the mouse.
    
    if printer:
        print(f'screenWidth={screenWidth} screenHeight={screenHeight}')
        print(f'currentMouseX={currentMouseX} currentMouseY={currentMouseY}')
    
    return [screenWidth, screenHeight, currentMouseX, currentMouseY]





## implementation examples
"""
pyautogui.moveTo(100, 150)

pyautogui.click()          # Click the mouse.
pyautogui.click(100, 200)  # Move the mouse to XY coordinates and click it.
pyautogui.click('button.png') # Find where button.png appears on the screen and click it.

pyautogui.move(400, 0)      # Move the mouse 400 pixels to the right of its current position.
pyautogui.doubleClick()     # Double click the mouse.
pyautogui.moveTo(500, 500, duration=2, tween=pyautogui.easeInOutQuad) # not needed
# Use tweening/easing function to move mouse over 2 seconds.

pyautogui.write('Hello world!', interval=0.01)  # type with quarter-second pause in between each key
pyautogui.press('esc')     # Press the Esc key. All key names are in pyautogui.KEY_NAMES

with pyautogui.hold('shift'):  # Press the Shift key down and hold it.
        pyautogui.press(['left', 'left', 'left', 'left'])  # Press the left arrow key 4 times.
# Shift key is released automatically.

pyautogui.press('tab')
pyautogui.hotkey('ctrl', 'c') # Press the Ctrl-C hotkey combination.

pyautogui.alert('This is the message to display.') # Make an alert box appear and pause the program until OK is clicked.


## SCREENSHOT

im = pyautogui.screenshot(region=(0,0, 300, 400))

"""
 