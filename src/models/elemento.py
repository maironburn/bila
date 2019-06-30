import os

class Element(object):
    _name = ''
    _image = ''
    _parent = None
    _x = 0.0
    _y = 0.0

    def __init__(self, kw):

        self._name = kw.get('_name')
        self._image = kw.get('_image')
        self._parent = kw.get('_parent')
        self._x = kw.get('_x')
        self._y = kw.get('_y')

    # <editor-fold desc="Getter y Setters">

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value:
            self._name = value

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):

        if value:
            self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if value:
            self._y = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        if value:
            self._image = value

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        if value:
            self._parent = value

    # </editor-fold>


class Boton(Element):
    _popscreen = None  # is container ?
    _popscreen_folder = None

    def __init__(self, kw):
        super().__init__(kw)
        self._popscreen = kw.get('popscreen')
        # self._child_screen = kw.get('child_screen')


class Tab(Element):
    _is_active = False
    _image_folder = None
    _is_mapped = False
    _elements = {}

    def __init__(self, kw):
        super().__init__(kw)
        self._image_folder="{}{}{}".format(os.path.abspath(os.path.join(self._image, os.pardir)), os.path.sep, self.name)
        self._elements = kw.get('_dict_elements', {})
        # self._child_screen = kw.get('child_screen')

    # <editor-fold desc="Getter / Setters">

    def add_element(self, element):
        if element:  # and issubclass(element, Elemento):
            self.elements.update({element.name: element})

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, value):
        if value:
            self._is_active = value

    @property
    def image_folder(self):
        return self._image_folder

    @image_folder.setter
    def image_folder(self, value):
        if value:
            self._image_folder = value

    @property
    def is_mapped(self):
        return self._is_mapped

    @is_mapped.setter
    def is_mapped(self, value):
        if value:
            self._is_mapped = value

    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, value):
        if value:
            self._elements = value
    # </editor-fold>


class Text(Element):

    def __init__(self, kw):
        super().__init__(kw)
        # self._child_screen = kw.get('child_screen')
