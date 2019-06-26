from common_config import TEMP_IMGS, MAPPED_WINDOWS, FOREGROUND_THREAD, SAVE_MAPPING
from settings.screen_schemes import windows_skels
import os
from os.path import sep as separator
from src.models.pantalla import Pantalla
from src.controllers.img_recognition import getElementCoords
from loggin.app_logger import AppLogger
from src.controllers.win_app_handler import WinAppHandler
import threading
import json
from src.controllers.doc_parser import Doc_Parser
from common_config import APP_NAME
from src.helpers.screen import screen_resolution, capture_screen
from src.helpers.common import dinamic_instance_elements, get_type_from_filename, \
    get_element_name_from_filename

from src.controllers.automation import insert_declarante
'''
import for testing
'''

#from src.controllers.workflow_translator import get_wf_parsed_data
'''class for window's elements mapping'''


class WinMapper(object):
    _current_window_name = None
    _win_app_handler = None
    _pantalla = None
    logger = None

    def __init__(self, kw):
        self.logger = AppLogger.create_log() if not self.logger else kw.get('logger')
        self._current_window_name = kw.get('current')
        if self._current_window_name:
            '''se instancia el controlador do not disturb'''
            if FOREGROUND_THREAD:
                self._win_app_handler = WinAppHandler(self.logger)
                if self._win_app_handler.handler:
                    daemon = threading.Thread(target=self._hwnd.daemon_dont_disturb_please).start()
                else:
                    self.logger.error("{} is not Running".format(APP_NAME))

            self.load_or_create_mapping()

    # mapper aux
    # in param: curwindows_name
    def map_window_ori(self):

        window = getattr(windows_skels, self._current_window_name)
        if windows_skels:
            self.pantalla = Pantalla(**window)
            self.load_elements()
            return self.pantalla

    def map_window(self):


        window = getattr(windows_skels, self._current_window_name)
        if windows_skels:
            self.pantalla = Pantalla(**window)

            while self.pantalla.parent:
                self.load_elements()
                return self.pantalla


    def load_elements(self):

        capture_screen() #''' debug purposes '''
        if os.path.exists(self.pantalla.image_folder):

            haystack = ("{}{}".format(TEMP_IMGS, "screenshot.png"))
            '''iterate over elements with non _ startswhith '''
            for filename in [x for x in os.listdir(self.pantalla.image_folder) if
                             not x.startswith('_') and os.path.isfile(
                                 "{}{}{}".format(self.pantalla.image_folder, separator, x))]:
                element_type = get_type_from_filename(filename)
                element_name = get_element_name_from_filename(filename)

                needle = "{}{}{}".format(self.pantalla.image_folder, separator, filename)
                ''' call to tesseract controller'''
                x, y = getElementCoords(haystack, needle)
                self.logger.info("{} -> located at x:{}, y:{}".format(element_name, x, y))
                kw = {'_name': element_name, '_image': needle, '_x': x, '_y': y, '_parent': self._current_window_name}

                '''building windows'''
                elm_instace = dinamic_instance_elements(element_type, kw)
                elm_instace and self.pantalla.add_element(elm_instace) or self.logger.error(
                    "elm_instace: {} Nulo".format(element_name))


            self.logger.info("{}".format(self.pantalla))

    '''check if app windows is already maped with the current dimensions'''

    def is_already_mapped(self):
        self.logger.info(
            "is_already_mapped ? -> Checking former map {}{}{}, h x w: {}".format(MAPPED_WINDOWS, os.path.sep,
                                                                                  self._current_window_name,
                                                                                  screen_resolution()))
        return os.path.exists(
            "{}{}{}{}".format(MAPPED_WINDOWS, separator, self._current_window_name, screen_resolution()))

    def load_or_create_mapping(self):

        try:
            if not self.is_already_mapped():
                '''Se mapean los elementos x reconocimiento de imgs'''
                self.map_window()
                '''serializamos y guardamos con el nombre la panta y su resolucion'''
                if SAVE_MAPPING:
                    self.pantalla.save_to_file(self._current_window_name, resolution=screen_resolution())
            else:
                '''Construccion de la pantalla a partir de los elementos persistidos en el fichero json'''
                with open("{}{}{}{}".format(MAPPED_WINDOWS, separator, self._current_window_name,
                                            screen_resolution())) as json_file:

                    kw = json.load(json_file)
                    json_element = kw.pop('_elements')
                    self.pantalla = Pantalla(**kw)
                    ''' deserializacion'''
                    for e in json_element.values():
                        self.pantalla.add_element(self.load_elements_from_json(e))

        except Exception as e:
            self.logger.error("Exception in {} load_or_create_mapping -> {}".format(self.__class__.__name__, e))

    def load_elements_from_json(self, element_dict):

        element_type = get_type_from_filename(element_dict.get('_image').split('\\')[-1])
        return dinamic_instance_elements(element_type, element_dict)

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
    winmaper = WinMapper({'current': 'nuevo_declarante'})
    pantalla = winmaper.pantalla
    '''
    elmt = pantalla.get_element_by_name('back')
    # obtencion de todos los elementos
    for k, v in pantalla.elements.items():
        print("elemento: {} --> x: {}, y: {}".format(k, v.x, v.y))
    '''

    kw = {'doc_src': 'macro_nueva_decarante.xls', 'args': pantalla.get_doc_parser_repr()}
    doc_parser = Doc_Parser(**kw)
    wf_parsed_data= doc_parser.get_wf_parsed_data()
    btn_aceptar= pantalla.get_element_by_name('aceptar')
    commit =btn_aceptar.x, btn_aceptar.y
    insert_declarante(wf_parsed_data,commit )
    # print("inspect me")
