import json
from os.path import sep as separator
from common_config import MAPPED_WINDOWS


class Pantalla(object):
    _name = ''
    _element_img_folder = None
    _elements = {}
    _parent = None
    _mapping_file = None

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

    def get_element_by_name(self, element_name):
        if self.has_element(element_name):
            return self.elements[element_name]

    def save_to_file(self, window_name, resolution):
        # @todo, refresh de las dimensiones de la ventana
        with open('{}{}{}{}'.format(MAPPED_WINDOWS, separator, window_name, resolution),
                  'w') as outfile:
            outfile.write("{}".format(self.__repr__()))

    def get_doc_parser_repr(self):
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
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        if value:
            self._parent = value

    # </editor-fold>
