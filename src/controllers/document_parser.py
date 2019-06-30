import pandas as pd
from common_config import WORKFLOWS
from os import path, sep
import sys


class Doc_Parser(object):
    _doc = None
    _df = pd.DataFrame
    _mapping = None

    def __init__(self, **kw):

        self.doc = "{}{}{}".format(WORKFLOWS, sep, kw.get('document'))
        ''' parametros adicionales del documento , delimitadores, indices '''
        args = kw.get('args', None)

        if path.exists(self.doc) and args:
            self.read_document_remap_columns(args)

    def read_document_remap_columns(self, args):

        ''' brief:
            carga el documento y remapea las columnas por sus coordenadas de posicion

            halla la correspondencia nombre de la columna -> elemento de ref en la app
            y resetea los nombres de las columnas por sus coordnadas cartesianas
        '''
        try:
            # self.df = self._reader(self.doc)
            self._df = pd.read_excel(self.doc, encoding=sys.getfilesystemencoding())
            new_index = []
            aditional_data = []
            for c in self._df.columns:
                if c and len(c):
                    if c in args.keys():
                        new_index.append(args[c])
                    else:
                        new_index.append(c)

            # esta comprobacion deberia ir arriba y evitar reindex si no hay correspondencia numerica de elementos
            if self._df.shape[1] == len(new_index):
                self._df.columns = new_index

        except Exception as e:
            print("{}".format(e))

    def get_type(self):
        return self._doc.split('.')[-1]

    def get_wf_parsed_data(self):

        extracted_data = []
        try:
            if not self.df is None:
                for index, row in self.df.iterrows():
                    data_list = []
                    for i in range(row.shape[0]):  # ''' num of columns'''
                        # print("{} -> {}".format(df.columns[i], row[i]))
                        if ',' in self.df.columns[i]:
                            data_list.append({'x': self.df.columns[i].split(',')[0],
                                              'y': self.df.columns[i].split(',')[1],
                                               self.df.columns[i]: row[i]})
                        else:
                            data_list.append({self.df.columns[i]: row[i]})
                    extracted_data.append(data_list)

            return extracted_data

        except Exception as e:
            pass

        return None

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
