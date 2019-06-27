from src.models import elemento
from src.models.pantalla import Pantalla
from settings.screen_schemes import windows_skels
from os.path import isfile, exists, sep as separator
from os import listdir
from common_config import TEMP_IMGS
from src.helpers.screen import capture_screen
from src.controllers.automation import go_back


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


def load_elements(self, pantalla):
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
            self.pantalla.add_element(self.create_element_instance(kw))
        ''' mapeada la pantalla va a la pantalla padre'''
        go_back(pantalla)
        self.logger.info("{}".format(pantalla))
        return pantalla


def get_ancestors_map(instance=None):
    ''' recursion ascendente para mapear las pantallas padres'''
    while instance.parent != None:
        pantalla = load_json_skel(instance.parent)
        load_elements(pantalla)
        instance.parent = pantalla

        return get_ancestors_map(instance.parent)
