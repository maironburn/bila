from os.path import sep as separator
from os.path import exists
from common_config import WORKFLOWS


def get_wf_parsed_data(df=None):

    extracted_data = {}
    try:
        if not df is None:
            for index, row in df.iterrows():
                extracted_data.update({index: ''})
                data_list = []
                for i in range(row.shape[0]):
                    #print("{} -> {}".format(df.columns[i], row[i]))
                    data_list.append({'x': df.columns[i].split(',')[0],
                                      'y': df.columns[i].split(',')[1],
                                      'payload': row[i]})

                extracted_data[index] = data_list

        return extracted_data

    except Exception as e:
        pass

    return None


def process_macro(sentence):
    print("process_macro")
    return "{}".format(sentence)


def read_and_start(filename='test.txt'):
    if exists(("{}{}{}".format(WORKFLOWS, separator, filename))):
        with open("{}{}{}".format(WORKFLOWS, separator, "test.txt"), 'r') as f:
            readed = f.readlines()

        sentences = map(process_macro, readed)
        print(sentences)
    return None


if __name__ == '__main__':
    read_and_start()
