# -*- coding: utf-8 -*-

import pyautogui
from pywinauto import keyboard
import pyperclip
from time import sleep


def where_screen_am_i():
    pass


def evaluate_action(kw=None):
    dict_actions = {
        'insert_declarante': insert_declarante
    }

    action = kw.get('action', None)

    if action:
        dict_actions[action](kw)


def active_tab(tabs_dict, tab_name):

    if len(tabs_dict.keys()) and tab_name in tabs_dict.keys():
        target = tabs_dict[tab_name]
        pyautogui.moveTo(target.x, target.y, 1)
        pyautogui.click()
        target.active = True


def goto_screen(screen_tree_obj, current_screen, target_screen):

    path_tree= None
    # while screen_tree_obj.parent:
    #     path_tree=
    #     btn_declarantes = screen_tree_obj.get_element_by_name('declarantes')
    # click_coods = btn_declarantes.x, btn_declarantes.y
    # pyautogui.moveTo(click_coods, 1)
    # pyautogui.click()
    # # sleep(2)


def goto_screen_ori(screen_tree_obj, element_name):

    btn_declarantes = screen_tree_obj.get_element_by_name('declarantes')
    click_coods = btn_declarantes.x, btn_declarantes.y
    pyautogui.moveTo(click_coods, 1)
    pyautogui.click()
    # sleep(2)


def go_back(pantalla):
    salir = pantalla.get_element_by_name('salir')
    if salir and pantalla.name != 'main':
        pyautogui.moveTo(salir.x, salir.y, 1)
        pyautogui.click()
        sleep(1)
        # capture screen


def insert_declarante(kw):
    # (payload, callback, commit=(), restart_op=()):

    # commit = btn_aceptar.x, btn_aceptar.y

    payload = kw.get('payload',
                     None)  # ''' datos con el nombre de las cols mapeados a sus correspondientes coords de elementos'''
    commit = kw.get('commit', None)  # ''' secuencia de pasos para concluir la insercion de los payloads'''
    reload = kw.get('reload', None)  # ''' si la accion acometida requiere pasos posteriores para reiterar la accion'''
    target_screen = kw.get('target_screen', None)  # ''' donde se realiza la operacion'''
    current_screen = kw.get('current_screen')
    screen_tree_obj = kw.get('screen_tree_obj')
    '''
    posicionamiento hacia la pantalla objetivo
    '''
    btn_declarantes = screen_tree_obj.get_element_by_name('target_screen')
    click_coods = btn_declarantes.x, btn_declarantes.y
    pyautogui.moveTo(click_coods, 1)
    pyautogui.click()
    # sleep(2)

    for elements in payload:
        for i in elements:
            pyautogui.moveTo(int(i.get('x')), int(i.get('y')), 1)
            pyautogui.doubleClick()
            pyperclip.copy(i.get('payload'))
            pyautogui.hotkey("ctrl", "v")

        pyautogui.moveTo(commit)
        pyautogui.click()
        return
