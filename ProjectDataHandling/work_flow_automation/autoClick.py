
import time 
import os

import pyautogui

import ProjectDataHandling.utils.click_automate as auto

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


def except_func(file, arg, i):
    # to edit auto 
    pyautogui.write(arg[i], interval=0.01)
    pyautogui.press('left')


class autoEngine():

    def __init__(self, PIC_FILES_DIR, except_cond=False, *args):
        
        self.arg = args
        self.PIC_DICT = PIC_FILES_DIR # DIR with the button pics
        self.pic_files = [f for f in os.listdir(self.PIC_DICT) if os.path.isfile(os.path.join(self.PIC_DICT, f))]

        self.except_cond = except_cond

    def auto_gui(self, except_func, wait=1, print=False, click=None):
        # except_func is the func for exceptions

        for i, file in enumerate(self.pic_files):
            if self.except_cond:
                except_func(file, self.arg, i)

            while click==None:
                click = click_button_from_picture(
                    os.path.join(self.PIC_DICT, file)
                )

            if print:
                print(f'step {click}')

            time.sleep(wait)
