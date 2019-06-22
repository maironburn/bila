from common_config import TEMP_IMGS, MAPED_WINDOWS
from settings.screen_schemes import windows
import os
from src.Models.Pantalla import Pantalla, Elemento
from src.Controllers.tesserator import getElementCoords
from loggin.AppLogger import AppLogger
from src.Controllers.win_app_handler import WinAppHandler
import json

'''class for window's elements mapping'''


class WinMaper(object):
    _current_window_name = None
    _hwnd = None
    _pantalla = None
    logger = None

    def __init__(self, kw):
        self.logger = AppLogger.create_log() if not self.logger else kw.get('logger')
        self._hwnd = WinAppHandler(self.logger)

        if self._hwnd.handler:
            self._hwnd.set_foreground(False)
            self._current_window_name = kw.get('current')
            # check was maped before ?
            if not self.is_already_mapped():
                pass
        else:
            self.logger.info("Bila is not Running")

    def map_window(self):

        window = getattr(windows, self._current_window_name)
        if windows:
            self.pantalla = Pantalla(**window)
            self.load_elements()
            return self._pantalla

    '''instantiating attending to element_type (inferred by the filename first _  )'''

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

    def load_elements(self):

        if os.path.exists(self.pantalla.image_folder):
            haystack = ("{}{}".format(TEMP_IMGS, "screenshot.png"))
            '''iterate over elements with non _ startswhith '''
            for filename in [x for x in os.listdir(self.pantalla.image_folder) if not x.startswith('_')]:
                element_type = self.get_type_from_filename(filename)
                element_name = self.get_element_name_from_filename(filename)
                needle = "{}{}{}".format(self.pantalla.image_folder, os.path.sep, filename)
                x, y = getElementCoords(haystack, needle)
                self.logger.info("{} -> located at x:{}, y:{}".format(element_name, x, y))
                kw = {'nombre': element_name, 'image': needle, 'x': x, 'y': y}
                elm_instace = self.dinamic_instance_elements(element_type, kw)
                self.pantalla.add_element(elm_instace)
            self.logger.info("{}".format(self.pantalla))

    '''check if app windows is already maped with the current dimensions'''

    def is_already_mapped(self):
        self.logger.info(
            "is_already_mapped ? -> Checking former map {}{}{}, h x w: {}".format(MAPED_WINDOWS, os.path.sep,
                                                                                  self._current_window_name,
                                                                                  self._hwnd.get_h_w))
        return os.path.exists(
            "{}{}{}{}".format(MAPED_WINDOWS, os.path.sep, self._current_window_name, self._hwnd.get_h_w))

    def save(self):
        pass

    # <editor-fold desc="Getter / Setter">
    @property
    def pantalla(self):
        return self._pantalla

    @pantalla.setter
    def pantalla(self, value):
        if value:
            self._pantalla = value
    # </editor-fold>


if __name__ == '__main__':
    winmaper = WinMaper({'current': 'main_window'})
    winmaper.map_window()
