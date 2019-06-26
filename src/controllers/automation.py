#-*- coding: utf-8 -*-

import pyautogui
from pywinauto import keyboard
import pyperclip

def insert_declarante(payload, commit=(), restart_op=()):
    for elements in payload:
        for i in elements:
            pyautogui.moveTo(int(i.get('x')), int(i.get('y')),1)
            pyautogui.doubleClick()
            pyperclip.copy(i.get('payload'))
            pyautogui.hotkey("ctrl", "v")

        pyautogui.moveTo(commit)
        pyautogui.click()
        return
