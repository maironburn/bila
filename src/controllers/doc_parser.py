import pandas as pd
import numpy
from common_config import WORKFLOWS
from os import path, sep


class Doc_Parser(object):

    _doc = None
    _reader = None
    _dataframe = None

    dict_reader = {'xls': pd.read_excel,
                   'csv': pd.read_csv}

    def __init__(self, **kw):

        self.doc = "{}{}{}".format(WORKFLOWS, sep, kw.get('doc_src'))
        if path.exists(self.doc):
            args = kw.get('args')
            self._reader = self.dict_reader[self.get_type()]
            self.load_document(args)

    # parametros adicionales del documento , delimitadores, indices
    def load_document(self, args=None):

        self.dataframe = self._reader(self.doc)
        print("")

    def map_columns():
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
    def reader(self):
        return self._reader

    @reader.setter
    def reader(self, value):
        if value:
            self._reader = value

    @property
    def dataframe(self):
        return self._dataframe

    @dataframe.setter
    def dataframe(self, value):
        if value:
            self._dataframe = value
    # </editor-fold>
