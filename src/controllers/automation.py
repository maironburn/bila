# -*- coding: utf-8 -*-

import pyautogui
from pywinauto import keyboard
import pyperclip
from time import sleep



def where_screen_am_i ():
    pass


def evaluate_action(kw=None):
    dict_actions = {
        'insert_declarante': insert_declarante

    }
    action = kw.get('action', None)

    if action:
        dict_actions[action](kw)



def goto_screen():
    pass


def go_back(pantalla):

    salir = pantalla.get_element_by_name('salir')
    if salir and pantalla.name != 'main':
        pyautogui.moveTo(salir.x, salir.y, 1)
        pyautogui.click()
        sleep(1)

def insert_declarante(kw):
    #(payload, callback, commit=(), restart_op=()):

    #commit = btn_aceptar.x, btn_aceptar.y

    payload = kw.get('payload', None)
    commit =  kw.get('commit', None)
    reload =  kw.get('reload', None)
    obj_pantalla = kw.get('obj_pantalla', None)
    current_screen = kw.get('')

    '''
    posicionamiento hacia la pantalla objetivo
    '''
    btn_declarantes= obj_pantalla.get_element_by_name('declarantes')
    click_coods=  btn_declarantes.x, btn_declarantes.y
    pyautogui.moveTo(click_coods, 1)
    pyautogui.click()
    #sleep(2)


    for elements in payload:
        for i in elements:
            pyautogui.moveTo(int(i.get('x')), int(i.get('y')), 1)
            pyautogui.doubleClick()
            pyperclip.copy(i.get('payload'))
            pyautogui.hotkey("ctrl", "v")

        pyautogui.moveTo(commit)
        pyautogui.click()
        return
