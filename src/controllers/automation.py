# -*- coding: utf-8 -*-

import pyautogui
from pywinauto import keyboard
import pyperclip
from time import sleep
from src.models.elemento import Tab


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
    from src.helpers.screen_mapper import load_elements
    if len(tabs_dict.keys()) and tab_name in tabs_dict.keys():

        target = tabs_dict[tab_name]
        for tabs in tabs_dict.values():
            tabs.is_active = False
        pyautogui.moveTo(target.x, target.y)
        pyautogui.click()
        target.is_active = True
        if not target.is_mapped:
            load_elements(target, get_back=False)
            target.is_mapped = True
            sleep(1)


def goto_screen_ori(screen, path=None):
    from src.helpers.screen_mapper import load_json_skel, load_elements
    from src.helpers.screen_mapper import get_element_by_name_at_tree

    path_tree = path.split('.')
    from src.helpers.screen_mapper import get_element_by_name_at_tree
    for p in path_tree:
        element = get_element_by_name_at_tree(screen, p)
        pyautogui.moveTo(element.x, element.y, 1)
        pyautogui.click()
        # element = get_element_by_name_at_tree(screen, p)
        # pyautogui.moveTo(element.x, element.y, 1)
        # pyautogui.click()
        # #screen =
        # pantalla = load_json_skel(p)
        # load_elements(pantalla)


def goto_screen(screen, path=None):
    from src.helpers.screen_mapper import load_json_skel, load_elements

    if path and isinstance(path, str):
        path = path.split('.')

    if len(path) > 1:
        root = path.pop(0)
        pantalla = load_json_skel(root)
        screen = load_elements(pantalla, get_back=False)
        element_name = path.pop(0)
        element = screen.get_element_by_name(element_name)
        print("searching in screen : {}, el elemento: {}".format(screen.name, element_name))
        move_to_element(element)

        pantalla = load_json_skel(element_name)
        screen = load_elements(pantalla, get_back=False)
        sleep(1)
        return goto_screen(pantalla, path)

    else:
        element_name = path.pop(0)
        element = screen.get_element_by_name(element_name)
        move_to_element(element)
        pantalla = load_json_skel(element_name)
        screen = load_elements(pantalla, get_back=False)


    return screen


def move_to_element(element):
    if element:
        pyautogui.moveTo(element.x, element.y)
        pyautogui.click()
        sleep(1)

def go_back(pantalla):
    salir = pantalla.get_element_by_name('salir')
    if salir and pantalla.name != 'main':
        pyautogui.moveTo(salir.x, salir.y, 1)
        pyautogui.click()
        sleep(1)
        # capture screen


def action_block(pantalla):
    tabs = pantalla.get_dict_elements_from_type(Tab)
    active_tab(tabs, 'actividades')


def special_treatement_required(dato):
    pass


def insert_declarante(kw):
    # (payload, callback, commit=(), restart_op=()):

    # commit = btn_aceptar.x, btn_aceptar.y

    # la accion de add un telef comprende:
    # - activar el tab correspondiente /telf_email
    # - hacer click sobre el boton de add
    # - (se abre la ventana, capturarla)
    # - identificar el textbox y check de predeterminado
    # - click de aceptar

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
    # btn_declarantes = screen_tree_obj.get_element_by_name('target_screen')
    # click_coods = btn_declarantes.x, btn_declarantes.y
    # pyautogui.moveTo(click_coods, 1)
    # pyautogui.click()
    # sleep(2)

    for elements in payload:
        treatement_required = []
        for i in elements:
            if 'x' in i.keys() and 'y' in i.keys():
                pyautogui.moveTo(int(i.get('x')), int(i.get('y')), 1)
                pyautogui.doubleClick()
                pyperclip.copy(i.get('payload'))
                pyautogui.hotkey("ctrl", "v")
            else:
                treatement_required.append(i)

        special_treatement_required(treatement_required)

        pyautogui.moveTo(commit)
        pyautogui.click()
        return
