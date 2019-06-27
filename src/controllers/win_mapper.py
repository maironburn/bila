from common_config import TEMP_IMGS, MAPPED_WINDOWS, FOREGROUND_THREAD, SAVE_MAPPING
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
from src.helpers.screen_mapper import dinamic_instance_elements, get_type_from_filename, \
    get_element_name_from_filename, load_json_skel
import pyautogui
from src.controllers.automation import evaluate_action, go_back

'''
import for testing
'''

# from src.controllers.workflow_translator import get_wf_parsed_data
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
            self.pantalla = load_json_skel(self._current_window_name)
            self.load_elements(self.pantalla)

            '''se instancia el controlador do not disturb'''
            if FOREGROUND_THREAD:
                self._win_app_handler = WinAppHandler(self.logger)
                if self._win_app_handler.handler:
                    daemon = threading.Thread(target=self._hwnd.daemon_dont_disturb_please).start()
                else:
                    self.logger.error("{} is not Running".format(APP_NAME))

            self.load_or_create_mapping()

    def get_ancestors_map(self, instance=None):
        ''' recursion ascendente para mapear las pantallas padres'''
        while instance.parent != None:
            pantalla = load_json_skel(instance.parent)
            self.load_elements(pantalla)
            instance.parent = pantalla

            return self.get_ancestors_map(instance.parent)

    def create_element_instance(self, kw):
        ''' Instancia a los elementos componentes de la pantalla
            a partir de la imagen del dataset se obtiene el tipo de elemento
            y su nombre...
            p_ej: boton_declarantes --> tipo: boton, nombre: declarante
        '''
        filename = kw.get('filename')
        haystack = kw.get('haystack')
        pantalla = kw.get('pantalla')
        element_type = get_type_from_filename(filename)
        element_name = get_element_name_from_filename(filename)
        needle = "{}{}{}".format(pantalla.image_folder, separator, filename)
        ''' call to tesseract controller'''
        x, y = getElementCoords(haystack, needle)
        self.logger.info("{} -> located at x:{}, y:{}".format(element_name, x, y))
        kw = {'_name': element_name, '_image': needle, '_x': x, '_y': y, '_parent': pantalla.parent}
        '''building windows'''

        elm_instace = dinamic_instance_elements(element_type, kw)
        elm_instace and pantalla.add_element(elm_instace) or self.logger.error(
            "elm_instace: {} Nulo".format(element_name))

    def load_elements(self, pantalla):

        ''' Carga los elemnetos integrantes de la pantalla
            mapeados en recursion ascendente
        '''
        haystack = ("{}{}.png".format(TEMP_IMGS, pantalla.name))
        capture_screen(pantalla.name)
        if os.path.exists(pantalla.image_folder):
            '''iterate over elements with non _ startswhith '''
            for filename in [x for x in os.listdir(pantalla.image_folder) if
                             not x.startswith('_') and os.path.isfile(
                                 "{}{}{}".format(pantalla.image_folder, separator, x))]:
                kw = {'filename': filename, 'pantalla': pantalla, 'haystack': haystack}
                self.pantalla.add_element(self.create_element_instance(kw))
            ''' mapeada la pantalla va a la pantalla padre'''
            go_back(pantalla)
            self.logger.info("{}".format(pantalla))
            return pantalla

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
                self.get_ancestors_map(self.pantalla)
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

    def get_element_by_name_at_tree(self, pantalla, name):

        element = pantalla.get_element_by_name(name)
        if element:
            return element
        else:
            return self.get_element_by_name_at_tree(pantalla.parent, name)

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

    btn_declarantes = winmaper.get_element_by_name_at_tree(pantalla, 'declarantes')
    pyautogui.moveTo(btn_declarantes.x, btn_declarantes.y, 1)
    pyautogui.click()

    kw = {'doc_src': 'macro_nueva_decarante.xls', 'args': pantalla.get_doc_parser_repr()}
    doc_parser = Doc_Parser(**kw)
    wf_parsed_data = doc_parser.get_wf_parsed_data()
    btn_aceptar = pantalla.get_element_by_name('aceptar')

    kw = {'payload': wf_parsed_data, 'callback': None,
          'action': 'insert_declarante', 'obj_pantalla': pantalla,
          'current_screen': 'main',
          'action_screen': 'nuevo_declarante'}
    evaluate_action(kw)
    # print("inspect me")
