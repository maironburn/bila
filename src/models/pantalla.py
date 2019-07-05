import json
from os.path import sep as separator
from common_config import MAPPED_WINDOWS
from src.models.elemento import Tab, Boton


class Pantalla(object):
    _name = ''
    _element_img_folder = None
    _elements = {}
    _parent = None
    _mapping_file = None
    _childrens = {}

    def __init__(self, **kw):
        self._name = kw.get('_name')
        self._element_img_folder = kw.get('_img_folder')
        self._elements = kw.get('_dict_elements', {})
        self._parent = kw.get('_parent')

    def add_element(self, element):
        if element:  # and issubclass(element, Elemento):
            self.elements.update({element.name: element})

    def has_element(self, element_name):
        return element_name in self.elements.keys()

    def has_childrens(self):
        return len(self.childrens.keys())

    def add_children(self, screen):
        if screen and isinstance(screen, Pantalla):
            self.childrens.update({screen.name: screen})


    def get_element_by_name(self, element_name):
        if self.has_element(element_name):
            return self.elements[element_name]
        return None

    def get_root(self, root=None):

        if root.parent:
            root = root.parent
            return self.get_root(root)

        return root

    def get_dict_elements_from_type(self, element_type):
        '''get dictionary k: nombre, v: instance of type
            on the current level (no recursion...at the moment, dont know if could be neccesary further on
        '''
        dict_elements = {}
        if self.elements:
            for e in self.elements:
                if type(self.elements[e]) is element_type:
                    dict_elements.update({e: self.elements[e]})
            # return [self.elements[x] for x in self.elements if type(self.elements[x]) is element_type]

        return dict_elements

    def get_active_tab(self):
        for e in self.elements:
            if isinstance(self.elements[e], Tab) and self.elements[e].is_active:
                return self.elements[e]

        return None

    def get_tab_names(self):
        '''listado de elementos de tipo tab'''
        tabs_name = []
        for e in self.elements:
            if isinstance(self.elements[e], Tab):
                tabs_name.append(e)

        return tabs_name

    def set_all_tab_inactive(self):
        for e in self.elements:
            if isinstance(self.elements[e], Tab):
                self.elements[e].is_active = False


    def save_to_file(self, window_name, resolution):
        # @todo, refresh de las dimensiones de la ventana
        with open('{}{}{}{}'.format(MAPPED_WINDOWS, separator, window_name, resolution),
                  'w') as outfile:
            outfile.write("{}".format(self.__repr__()))

    def get_document_mapped_columns_to_coord(self):
        '''
            devuelve las coordenadas x,y de cada Elemnto de la lista de elementos
            para que el automatismo realice las acciones oportunas
        '''

        doc_parser_repr = {}
        for k, v in self.elements.items():
            if v:
                doc_parser_repr.update({k: '{},{}'.format(v.x, v.y)})

        return doc_parser_repr

    def __repr__(self):
        return json.dumps(self, default=lambda x: x.__dict__,
                          sort_keys=True, indent=4)

    # <editor-fold desc="Getters y Setters">
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value:
            self._name = value

    @property
    def image_folder(self):
        return self._element_img_folder

    @image_folder.setter
    def image_folder(self, value):
        if value:
            self._element_img_folder = value

    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, value):
        if value:
            self._elements = value

    @property
    def childrens(self):
        return self._childrens

    @elements.setter
    def childrens(self, value):
        if value:
            self._childrens = value


    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        if value:
            self._parent = value

    # </editor-fold>

class Popscreen(Pantalla):

    def __init__(self, kw):
        super().__init__(kw)