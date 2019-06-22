from . import Elemento


class Pantalla(object):
    _nombre = ''
    _image_folder = None
    _elementos = {}

    def __init__(self, **kw):
        self._nombre = kw.get('nombre')
        self._image_folder = kw.get('img_folder')
        self._elementos = kw.get('dict_elementos')

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
    # </editor-fold>

    def add_element(self, element):
        if element:
            self.elementos.update({element.nombre: element})