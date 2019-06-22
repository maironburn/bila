from . import Elemento


class Pantalla(object):
    _nombre = ''
    _image_folder = None
    _elementos = {}
    _parent = None
    _maping_file = None

    def __init__(self, **kw):
        self._nombre = kw.get('nombre')
        self._image_folder = kw.get('img_folder')
        self._elementos = kw.get('dict_elementos')
        self._parent = kw.get('parent')
        self._parent = kw.get('parent')

    def add_element(self, element):
        if element:
            self.elementos.update({element.nombre: element})

    def has_element(self, element_name):
        return element_name in self.elementos.keys()

    def get_element_by_name(self, element_name):
        if element_name and element_name in self.elementos.keys():
            return self.elementos[element_name]

    def save(self):
        pass

    # <editor-fold desc="Getters y Setters">
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, value):
        if value:
            self._nombre = value

    @property
    def image_folder(self):
        return self._image_folder

    @image_folder.setter
    def image_folder(self, value):
        if value:
            self._image_folder = value

    @property
    def elementos(self):
        return self._elementos

    @elementos.setter
    def elementos(self, value):
        if value:
            self._elementos = value

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        if value:
            self._parent = value

    # </editor-fold>
