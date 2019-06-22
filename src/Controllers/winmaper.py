from common_config import TEMP_IMGS, MAPED_WINDOWS
from settings.screen_schemes import windows
import os
from src.Models.Pantalla import Pantalla, Elemento
from src.Controllers.tesserator import getElementCoords
from loggin.AppLogger import AppLogger
from src.Controllers.win_app_handler import WinAppHandler


class WinMaper(object):
    _current_window = None
    _hwnd = None

    def __init__(self, kw):

        self.logger = AppLogger.create_log()
        self._hwnd = WinAppHandler()

        if self._hwnd.handler:
            self._hwnd.set_foreground(False)
            self._current_window = kw.get('current')
        # else -> no esta en ejecucion
        # check is maped?
        if not self.is_already_maped():
            pass


    def map_window(self, winname):

        window = getattr(windows, winname)
        if windows:
            pantalla = Pantalla(**window)
            self.load_elements(pantalla)
            return pantalla

    '''instantiating atending to element_type (infered by the filename first _'''

    def dinamic_instance_elements(self, element_type, init_values):
        try:
            element_type = getattr(Elemento, element_type)
            return element_type(init_values)

        except Exception as e:
            pass

        return None

    def get_type_from_filename(self, filename):
        return filename.split('_')[0].capitalize()

    '''element name without extension neither type'''

    def get_element_name_from_filename(self, filename):
        return filename[0:filename.index('.')][filename.index('_') + 1:]

    def dump_config_window(self):
        pass

    def load_elements(self, pantalla):

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

    '''check if app windows is already maped with the current dimensions'''
    def is_already_maped(self):
        return os.path.exists("{}{}{}{}".format(MAPED_WINDOWS, os.path.sep,self._current_window, self._hwnd.get_h_w))


if __name__ == '__main__':
    winmaper = WinMaper({'current': 'main_window'})
