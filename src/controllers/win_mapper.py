from common_config import TEMP_IMGS, MAPPED_WINDOWS
from settings.screen_schemes import windows_skels
import os
from os.path import sep as separator
from src.models.pantalla import Pantalla, elemento
from src.controllers.img_recognition import getElementCoords
from loggin.app_logger import AppLogger
from src.controllers.win_app_handler import WinAppHandler
import threading
import json
from time import sleep

'''class for window's elements mapping'''


class WinMapper(object):
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
            # check was mapped before ?
            sleep(1)
            self.load_or_create_mapping()
            '''
            daemon = threading.Thread(target=self._hwnd.daemon_dont_disturb_please)
            daemon.start()
            '''
        else:
            self.logger.info("Bila is not Running")
            # instanciar...jay q descompilar class @todo

    def map_window(self):

        window = getattr(windows_skels, self._current_window_name)
        if windows_skels:
            self.pantalla = Pantalla(**window)
            self.load_elements()
            return self.pantalla

    '''instantiating attending to element_type (inferred by the filename first _  )'''

    def dinamic_instance_elements(self, element_type, init_values):
        try:
            element_type = getattr(elemento, element_type)
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
            for filename in [x for x in os.listdir(self.pantalla.image_folder) if
                             not x.startswith('_') and os.path.isfile(
                                 "{}{}{}".format(self.pantalla.image_folder, separator, x))]:
                element_type = self.get_type_from_filename(filename)
                element_name = self.get_element_name_from_filename(filename)
                needle = "{}{}{}".format(self.pantalla.image_folder, separator, filename)
                ''' call to tesseract controller'''
                x, y = getElementCoords(haystack, needle)
                self.logger.info("{} -> located at x:{}, y:{}".format(element_name, x, y))
                kw = {'name': element_name, 'image': needle, 'x': x, 'y': y, '_parent': self.pantalla.name}
                '''building windows'''
                elm_instace = self.dinamic_instance_elements(element_type, kw)
                self.pantalla.add_element(elm_instace)
            self.logger.info("{}".format(self.pantalla))

    '''check if app windows is already maped with the current dimensions'''

    def is_already_mapped(self):
        self.logger.info(
            "is_already_mapped ? -> Checking former map {}{}{}, h x w: {}".format(MAPPED_WINDOWS, os.path.sep,
                                                                                  self._current_window_name,
                                                                                  self._hwnd.get_h_w))
        return os.path.exists(
            "{}{}{}{}".format(MAPPED_WINDOWS, separator, self._current_window_name, self._hwnd.get_h_w))

    def load_or_create_mapping(self):
        if not self.is_already_mapped():
            '''Se mapean los elementos x reconocimiento de imgs'''
            self.map_window()
            '''serializamos y guardamos con el nombre la panta y su resolucion'''
            self.save()
        else:
            '''Construccion de la pantalla a partir de los elementos persistidos en el fichero json'''
            with open("{}{}{}{}".format(MAPPED_WINDOWS, separator, self._current_window_name,
                                        self._hwnd.get_h_w)) as json_file:

                kw = json.load(json_file)
                json_element = kw.pop('_elements')
                self.pantalla = Pantalla(**kw)
                ''' deserializacion'''
                for e in json_element.values():
                    self.pantalla.add_element(self.load_elements_from_json(e))

    def save(self):
        # @todo, refresh de las dimensiones de la ventana
        with open('{}{}{}{}'.format(MAPPED_WINDOWS, separator, self._current_window_name, self._hwnd.get_h_w),
                  'w') as outfile:
            outfile.write("{}".format(self.pantalla))

    def load_elements_from_json(self, element_dict):

        element_type = self.get_type_from_filename(element_dict.get('_image').split('\\')[-1])
        return self.dinamic_instance_elements(element_type, element_dict)

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
    winmaper = WinMapper({'current': 'main'})
    pantalla = winmaper.pantalla
    elmt = pantalla.get_element_by_name('copia_seguridad')
    # print("x: {}, y: {}".format(elmt.x, elmt.y))

    # obtencion de todos los elementos
    for k, v in pantalla.elements.items():
        print("elemento: {} --> x: {}, y: {}".format(k, v.x, v.y))

    # print("inspect me")
