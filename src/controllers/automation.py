# -*- coding: utf-8 -*-

import pyautogui
from pywinauto import keyboard
import pyperclip



def where_screen_am_i (){

}

def evaluate_action(kw=None):
    dict_actions = {
        'insert_declarante': insert_declarante

    }
    action = kw.get('action', None)

    if action:
        dict_actions[action](kw)


def insert_declarante(payload, callback, commit=(), restart_op=()):
    for elements in payload:
        for i in elements:
            pyautogui.moveTo(int(i.get('x')), int(i.get('y')), 1)
            pyautogui.doubleClick()
            pyperclip.copy(i.get('payload'))
            pyautogui.hotkey("ctrl", "v")

        pyautogui.moveTo(commit)
        pyautogui.click()
        return
