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


def action_block(pantalla, tab_name):
    tabs = pantalla.get_dict_elements_from_type(Tab)
    active_tab(tabs, tab_name)


def special_treatement_required(pantalla, data):
    from src.helpers.screen_mapper import load_json_skel, load_elements
    action_block(pantalla, 'telef_email')
    element = pantalla.elements['telf_email'].elements['add_telefono']
    pyautogui.moveTo(element.x, element.y)
    pyautogui.click()
    sleep(1)

    pantalla = load_json_skel('popscreen_add_telf')
    screen = load_elements(pantalla, get_back=False)

    for d in data:
        if 'telefono' in d.keys():
            telf = screen.elements['telef']
            pyautogui.moveTo(telf.x, telf.y)
            pyautogui.doubleClick()
            pyperclip.copy(d.get('telefono'))
            pyautogui.hotkey("ctrl", "v")

        if 'telefono predeterminado' in d.keys():
            if d.get('telefono predeterminado').lower() == 'si':
                telf = screen.elements['telef_predeterminado']
                pyautogui.moveTo(telf.x, telf.y)
                pyautogui.click()

    aceptar = screen.elements['aceptar']
    pyautogui.moveTo(aceptar.x, aceptar.y)
    pyautogui.click()


def insert_declarante(kw):
    # (payload, callback, commit=(), restart_op=()):
    from src.helpers.screen_mapper import load_json_skel, load_elements
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

    for elements in payload:
        treatement_required = []
        for i in elements:
            if 'x' in i.keys() and 'y' in i.keys():
                pyautogui.moveTo(int(i.get('x')), int(i.get('y')))
                pyautogui.doubleClick()
                pyperclip.copy(i.get('payload'))
                pyautogui.hotkey("ctrl", "v")
            else:
                treatement_required.append(i)

        special_treatement_required(screen_tree_obj, treatement_required)

        commit = screen_tree_obj.elements['aceptar']
        pyautogui.moveTo(commit.x, commit.y)
        pyautogui.click()
        sleep(1)
        ''' reload '''
        pantalla = load_json_skel('declarantes')
        screen = load_elements(pantalla, get_back=False)
        sleep(1)
        reload = screen.elements['nuevo_declarante']
        pyautogui.moveTo(reload.x, reload.y)
        pyautogui.click()

        print("reload")
