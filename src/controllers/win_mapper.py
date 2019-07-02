from common_config import  MAPPED_WINDOWS, FOREGROUND_THREAD, SAVE_MAPPING
import os
from os.path import sep as separator
from src.models.pantalla import Pantalla

from loggin.app_logger import AppLogger
from src.controllers.dnd_daemon import WinAppHandler
import threading
import json
from src.controllers.document_parser import Doc_Parser
from common_config import APP_NAME
from src.helpers.screen import screen_resolution
from src.helpers.screen_mapper import dinamic_instance_elements, get_type_from_filename, \
    load_json_skel, load_elements, get_ancestors_map


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
            load_elements(self.pantalla)
            '''se instancia el controlador do not disturb'''
            if FOREGROUND_THREAD:  # el metodo no me des calor deberia ser static
                self._win_app_handler = WinAppHandler(self.logger)
                if self._win_app_handler.handler:
                    daemon = threading.Thread(target=self._hwnd.daemon_dont_disturb_please).start()
                else:
                    self.logger.error("{} is not Running".format(APP_NAME))

            self.load_or_create_mapping()

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
                get_ancestors_map(
                    self.pantalla)  # <------------------------------ comentado para probar la activacion de tabs
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

    @staticmethod
    def load_elements_from_json(element_dict):

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
    from src.controllers.automation import evaluate_action, go_back, active_tab, goto_screen
    from src.helpers.screen_mapper import map_tabs

    winmaper = WinMapper({'current': 'main'})
    pantalla = winmaper.pantalla
    pantalla = goto_screen(pantalla, "main.declarantes.nuevo_declarante")
    #goto_screen(pantalla, "main.declarantes.nuevo_declarante")
    map_tabs (pantalla)

    # pte de desactivar los map
    # bloque de acciones en automation para datos especiales
    #
    #nankw = {'document': 'macro_nannueva_decarante.xls', 'args': pantalla.get_document_mapped_columns_to_coord()}
    kw = {'document': 'macro_nueva_declarante_domicilio_telef.xls', 'args': pantalla.get_document_mapped_columns_to_coord()}

    doc_parser = Doc_Parser(**kw)
    wf_parsed_data = doc_parser.get_wf_parsed_data()
    # btn_aceptar = pantalla.get_element_by_name('aceptar')

    kw = {'payload': wf_parsed_data, 'callback': None,
          'action': 'insert_declarante', 'screen_tree_obj': pantalla,
          'current_screen': 'main',
          'target_screen': 'nuevo_declarante'}
    evaluate_action(kw)

    # print("inspect me")
