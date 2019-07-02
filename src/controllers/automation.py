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


def load_fill_screen(screen_name):
    from src.helpers.screen_mapper import load_json_skel, load_elements
    pantalla = load_json_skel(screen_name)
    return load_elements(pantalla, get_back=False)


def goto_screen(screen, path=None):
    if path and isinstance(path, str):
        path = path.split('.')

    if len(path) > 1:
        ''' estructura pantalla.elemento...'''
        root = path.pop(0)
        screen = load_fill_screen(root)
        element = path.pop(0)
        move_to_element(screen.get_element_by_name(element))
        screen = load_fill_screen(element)
        return goto_screen(screen, path)

    if path:
        element_name = path.pop(0)
        element = screen.get_element_by_name(element_name)
        move_to_element(element)
        return load_fill_screen(element_name)


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


def nuevo_declarante_tab_action(tab_name, add_button, popscreen):
    action_block(pantalla, tab_name)
    element = pantalla.elements[tab_name].elements[add_button]
    pyautogui.moveTo(element.x, element.y)
    pyautogui.click()
    sleep(1)
    pantalla = load_json_skel(popscreen)

    return load_elements(pantalla, get_back=False)


def autofill_data_popscreen(data, dict_key, pantalla):
    for data in data[dict_key]:
        for k, v in data.items():

            if k == 'prederminado' and v.lower() == 'si':
                elemento = pantalla.get_element_by_name('prederminado')
                pyautogui.moveTo(elemento.x, elemento.y)
                pyautogui.click()
                # pyautogui.hotkey("ctrl", "v")

            else:
                elemento = pantalla.get_element_by_name(k)
                pyautogui.moveTo(elemento.x, elemento.y)
                pyautogui.doubleClick()
                pyautogui.typewrite(str(v), 0.05)

    commit = pantalla.get_element_by_name('aceptar')
    pyautogui.moveTo(commit.x, commit.y)
    pyautogui.click()


def special_treatement_required(pantalla, data):
    from src.helpers.screen_mapper import load_json_skel, load_elements

    if len(data['domicilio_data']):
        screen = nuevo_declarante_tab_action('domicilio', 'add_common', 'popscreen_add_domicilio')
        autofill_data_popscreen(data, 'domicilio_data', pantalla)

    if len(data['telf_data']):
        screen = nuevo_declarante_tab_action('telf_email', 'add_telefono', 'popscreen_add_telf')
        autofill_data_popscreen(data, 'telf_data', pantalla)


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
        treatement_required = clasify_data(elements)
        for i in elements:
            if 'x' in i.keys() and 'y' in i.keys():
                pyautogui.moveTo(int(i.get('x')), int(i.get('y')))
                pyautogui.doubleClick()
                pyperclip.copy(i.get('payload'))
                pyautogui.hotkey("ctrl", "v")

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


def clasify_data(payload):
    from src.helpers.screen_mapper import get_element_name_from_filename

    special_data = {'domicilio_data': [],
                    'telf_data': []
                    }

    for e in payload:
        for key, value in e.items():  # iter on both keys and values
            if key and key.startswith('domicilio'):
                special_data['domicilio_data'].append({''.join(key.split('_')[1:]): value})

            if key and key.startswith('telefono'):
                special_data['telf_data'].append({''.join(key.split('_')[1:]): value})

    return special_data
