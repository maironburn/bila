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

    def __init__(self,kw):
        super().__init__(kw)
        #self._child_screen = kw.get('child_screen')


class Tab(Element):

    def __init__(self, **kw):
        super().__init__(kw)
        #self._child_screen = kw.get('child_screen')
