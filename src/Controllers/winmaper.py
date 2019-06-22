from common_config import TEMP_IMGS
import settings
from settings.screen_schemes import windows
from importlib import import_module
import os
from src.Models.Pantalla import Pantalla, Elemento
from src.Controllers.tesserator import getElementCoords

def map_window(winname):
    window = getattr(windows, winname)
    if windows:
        pantalla = Pantalla(**window)
        load_elements (pantalla)
        return pantalla

def dinamic_instance_elements(element_type,init_values):

    try:
        element_type=getattr(Elemento, element_type)
        return element_type(init_values)

    except Exception as e:
        pass

    return None

def get_type_from_filename(filename):
    return filename.split('_')[0].capitalize()

def get_element_name_from_filename(filename):
    return filename.split('_')[1:][0].split('.')[0]

def dump_config_window():
    pass

def load_elements(pantalla):

    if os.path.exists(pantalla.image_folder):
        haystack = ("{}{}".format(TEMP_IMGS, "screenshot.png"))
        for filename in os.listdir(pantalla.image_folder):

            element_type=get_type_from_filename(filename)
            element_name=get_element_name_from_filename(filename)
            needle = "{}{}{}".format(pantalla.image_folder, os.path.sep, filename)
            x, y = getElementCoords(haystack, needle)
            kw={'nombre': element_name, 'image': needle, 'x': x, 'y': y}
            elm_instace= dinamic_instance_elements(element_type,kw)
            #pantalla.elementos[]
            pantalla.add_element(elm_instace)

if __name__ == '__main__':
    map_window('main_window')
