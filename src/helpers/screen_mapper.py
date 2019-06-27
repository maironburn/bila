from src.models import elemento
from src.models.pantalla import Pantalla
from settings.screen_schemes import windows_skels
from os.path import isfile, exists, sep as separator
from os import listdir
from common_config import TEMP_IMGS
from src.helpers.screen import capture_screen
from src.controllers.automation import go_back
from src.controllers.img_recognition import getElementCoords


def get_type_from_filename(filename):
    '''extract name until first _ cause it defines class type'''
    return filename.split('_')[0].capitalize()


def get_element_name_from_filename(filename):
    '''element name without extension neither type'''
    return filename[0:filename.index('.')][filename.index('_') + 1:]


def dinamic_instance_elements(element_type, init_values):
    '''instantiating attending to element_type (inferred by the filename first _  )'''
    try:
        # getattr(module, class_name)
        element_type = getattr(elemento, element_type)
        return element_type(init_values)

    except Exception as e:
        pass
    return None


def load_json_skel(pantalla_name):
    window = getattr(windows_skels, pantalla_name)
    if windows_skels:
        return Pantalla(**window)

    return None


def create_element_instance(kw):
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
    # logger.info("{} -> located at x:{}, y:{}".format(element_name, x, y))
    kw = {'_name': element_name, '_image': needle, '_x': x, '_y': y, '_parent': pantalla.parent}
    '''building windows'''

    elm_instance = dinamic_instance_elements(element_type, kw)
    elm_instance and pantalla.add_element(elm_instance)


def load_elements(pantalla):
    ''' Carga los elemnetos integrantes de la pantalla
        mapeados en recursion ascendente
    '''
    haystack = ("{}{}.png".format(TEMP_IMGS, pantalla.name))
    capture_screen(pantalla.name)
    if exists(pantalla.image_folder):
        '''iterate over elements with non _ startswhith '''
        for filename in [x for x in listdir(pantalla.image_folder) if
                         not x.startswith('_') and isfile(
                             "{}{}{}".format(pantalla.image_folder, separator, x))]:
            kw = {'filename': filename, 'pantalla': pantalla, 'haystack': haystack}
            pantalla.add_element(create_element_instance(kw))
        ''' mapeada la pantalla va a la pantalla padre'''
        go_back(pantalla)
        # self.logger.info("{}".format(pantalla))
        return pantalla


def get_element_by_name_at_tree(pantalla, name):
    element = pantalla.get_element_by_name(name)
    if element:
        return element
    else:
        return get_element_by_name_at_tree(pantalla.parent, name)
