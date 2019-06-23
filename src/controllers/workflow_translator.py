from os.path import sep as separator
from os.path import exists
from common_config import WORKFLOWS


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
