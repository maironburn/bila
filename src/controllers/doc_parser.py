import pandas as pd
from common_config import WORKFLOWS
from os import path, sep


class Doc_Parser(object):
    _doc = None
    _df = pd.DataFrame
    _mapping = None

    def __init__(self, **kw):

        self.doc = "{}{}{}".format(WORKFLOWS, sep, kw.get('doc_src'))
        ''' parametros adicionales del documento , delimitadores, indices '''
        args = kw.get('args', None)

        if path.exists(self.doc) and args:
            self.load_document(args)

    def load_document_remap_columns(self, args={}):

        ''' carga el documento y remapea las columnas por sus coordenadas de posicion

            halla la correspondencia nombre de la columna -> elemento de ref en la app
            y resetea los nombres de las columnas por sus coordnadas cartesianas
        '''
        try:
            # self.df = self._reader(self.doc)
            self._df = pd.read_excel(self.doc)
            new_index = []
            for c in self._df.columns:
                if c and len(c) and c in args.keys():
                    new_index.append(args[c])

            if self._df.shape[1] == len(new_index):
                self._df.columns = new_index
            print("")

        except Exception as e:
            print("{}".format(e))

    def map_columns(self):
        ''' read columns header and overwrite then for x,y of corresponding element '''
        pass

    def get_type(self):
        return self._doc.split('.')[-1]

    # <editor-fold desc="Getter / Setter">

    @property
    def doc(self):
        return self._doc

    @doc.setter
    def doc(self, value):
        if value:
            self._doc = value

    @property
    def df(self):
        return self._df

    @df.setter
    def df(self, value):
        if value:
            self._df = value

    @property
    def mapping(self):
        return self._mapping

    @mapping.setter
    def mapping(self, value):
        if value:
            self._mapping = value

    # </editor-fold>
