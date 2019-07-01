from src.models import elemento
from src.models.pantalla import Pantalla
from settings.screen_schemes import windows_skels
from os.path import isfile, exists, sep as separator
from os import listdir
from common_config import TEMP_IMGS
from src.helpers.screen import capture_screen
from src.controllers.automation import go_back
from src.controllers.img_recognition import getElementCoords
import os
from src.models.elemento import Tab


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
    try:
        window = getattr(windows_skels, pantalla_name)
        if windows_skels:
            return Pantalla(**window)
    except Exception as e:
        pass

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
    screen_related = None
    screen_related = os.path.sep.join(needle.split(os.path.sep)[:-1])
    parent_dir = os.path.abspath(os.path.join(needle, os.pardir))
    kw = {'_name': element_name, '_image': needle, '_x': x, '_y': y,
          '_parent': pantalla.parent, '_screen_related': screen_related}
    '''building windows'''

    elm_instance = dinamic_instance_elements(element_type, kw)
    elm_instance and pantalla.add_element(elm_instance)


def create_screen(kw):
    pass


def map_tabs(pantalla):
    from src.controllers.automation import active_tab
    tabs = pantalla.get_dict_elements_from_type(Tab)
    tab_names = pantalla.get_tab_names()
    for tb in tab_names:
        active_tab(tabs, tb)


def get_root(root=None):
    if root.parent:
        root = root.parent
        load_elements(root)
        for e in root.elements:
            p = load_json_skel(e)
            if p:
                load_elements(p)
        return get_root(root)

    return root


def load_elements(elemento_contenedor, get_back=True, callback=None, callback_args=None):
    ''' Carga los elemnetos VISIBLES integrantes de un elmento contenedor: pantalla, tab
        mapeados en recursion ascendente
    '''
    haystack = ("{}{}.png".format(TEMP_IMGS, elemento_contenedor.name))
    capture_screen(elemento_contenedor.name)
    if exists(elemento_contenedor.image_folder):
        '''iterate over first level elements with non _ startswhith '''
        for filename in [x for x in listdir(elemento_contenedor.image_folder) if
                         not x.startswith('_') and isfile(
                             "{}{}{}".format(elemento_contenedor.image_folder, separator, x))]:
            kw = {'filename': filename, 'pantalla': elemento_contenedor, 'haystack': haystack}
            elemento_contenedor.add_element(create_element_instance(kw))
        ''' mapeada la pantalla va a la pantalla padre'''
        # if
        if get_back:
            go_back(elemento_contenedor)  # <------------- comentado para probar la activacion de tabs
        # self.logger.info("{}".format(pantalla))
        return elemento_contenedor


def get_ancestors_map(instance=None):
    ''' recursion ascendente para mapear las pantallas padres'''
    while instance.parent:
        pantalla = load_json_skel(instance.parent)
        load_elements(pantalla)
        instance.parent = pantalla

        return get_ancestors_map(instance.parent)


def get_element_by_name_at_tree(pantalla, name):

    if pantalla:
        element = pantalla.get_element_by_name(name)
        if element:
            return element
        else:
            return get_element_by_name_at_tree(pantalla.parent, name)
