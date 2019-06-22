from common_config import TEMP_IMGS,MAPED_WINDOWS
import settings
from settings.screen_schemes import windows
from importlib import import_module
import os
from src.Models.Pantalla import Pantalla, Elemento
from src.Controllers.tesserator import getElementCoords
from win32api import GetSystemMetrics

class WinMaper(object):

    _current_window= None

    def __init__(self, **kw):
        self._current_window= kw.get('current')
        #check is maped?

    def is_maped_already(self):
        return os.path.exists("{}{}{}".format(MAPED_WINDOWS, os.path.sep, self._current_window))

    def map_window(self,winname):

        window = getattr(windows, winname)
        if windows:
            pantalla = Pantalla(**window)
            self.load_elements(pantalla)
            return pantalla

    def dinamic_instance_elements(self,element_type, init_values):
        try:
            element_type = getattr(Elemento, element_type)
            return element_type(init_values)

        except Exception as e:
            pass

        return None

    def get_type_from_filename(self,filename):
        return filename.split('_')[0].capitalize()

    '''obtiene el nombre del elemento sin tipo ni extension'''

    def get_element_name_from_filename(self,filename):
        return filename[0:filename.index('.')][filename.index('_') + 1:]

    def dump_config_window(self):
        pass

    def load_elements(self,pantalla):

        if os.path.exists(pantalla.image_folder):
            haystack = ("{}{}".format(TEMP_IMGS, "screenshot.png"))
            '''solo actuamos sobre elementos que no contengan un _ inicial'''
            for filename in [x for x in os.listdir(pantalla.image_folder) if not x.startswith('_')]:
                element_type = self.get_type_from_filename(filename)
                element_name = self.get_element_name_from_filename(filename)
                needle = "{}{}{}".format(pantalla.image_folder, os.path.sep, filename)
                x, y = getElementCoords(haystack, needle)
                kw = {'nombre': element_name, 'image': needle, 'x': x, 'y': y}
                elm_instace = self.dinamic_instance_elements(element_type, kw)
                # pantalla.elementos[]
                pantalla.add_element(elm_instace)


if __name__ == '__main__':

    print("Width =", GetSystemMetrics(0))
    print("Height =", GetSystemMetrics(1))

    winmaper= WinMaper({'current': 'main_window'})

