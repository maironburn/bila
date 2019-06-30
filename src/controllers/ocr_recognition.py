import argparse
import os

import pytesseract as pytesseract
from PIL import Image
from markdown.extensions.toc import slugify

from common_config import OUTPUT_FOLDER

#from extract_window import extract_window_screenshot


def convert_tesseract_data_to_dict(string_data, update_with_coord=True):
    data_list = []
    for line_num, line in enumerate(string_data.split("\n")):
        line_dict = {}
        if line_num == 0:
            headers = line.split("\t")
        else:
            for attrib_num, value in enumerate(line.split("\t")):
                line_dict.update({headers[attrib_num]: value})
            if line_dict.get("text").strip():  # hay muchos bloques de texto vacio detectados, que descartamos
                if update_with_coord:
                    line_dict.update(Coord(
                        x1=line_dict.get("left", 0),
                        y1=line_dict.get("top", 0),
                        x2=line_dict.get("left", 0) + line_dict.get("width", 0),
                        y2=line_dict.get("top", 0) + line_dict.get("height", 0),
                        name=slugify(line_dict.get("text").strip(), separator="_"),
                    ).__dict__)
                data_list.append(line_dict)
    return data_list


def ocr_recognition(path_image_from_search=None, string_to_search=""):
    if not path_image_from_search:
        #path_image_from_search = extract_window_screenshot()
        pass

    # result_to_string = pytesseract.image_to_string(Image.open(path_image_from_search))
    # result_to_boxes = pytesseract.image_to_boxes(Image.open(path_image_from_search))
    result_to_data = pytesseract.image_to_data(Image.open(path_image_from_search), lang="spa+bas+eng")
    list_data = convert_tesseract_data_to_dict(result_to_data)
    if list_data: # si no es 0, es decir, si ha encontrado algo de texto

        if string_to_search:
            list_data_with_matches=[]
            for data in list_data:
                if string_to_search in data.get("text", ""):
                    print(data)
                    list_data_with_matches.append(data)
                    return list_data_with_matches
        else:
            if list_data:
                if len(list_data)==1:
                    pass
                else:
                    pass
            else:
                pass # TODO no se ha encontrado ninguno


    with open(os.path.join(OUTPUT_FOLDER, "ocr_result_to_data.csv"), 'w') as outfile:
        outfile.write(result_to_data)
    result_to_osd = pytesseract.image_to_osd(Image.open(path_image_from_search))
    print("hola")


if __name__ == '__main__':
    print("Interfaz de reconocimiento de texto sobre imagen \n")
    parser = argparse.ArgumentParser(description='Interfaz de reconocimiento de texto sobre imagen')


    def file_choices(choices, filename):
        ext = os.path.splitext(filename)[1][1:]
        if ext not in choices or not ext:
            parser.error("Tipo de archivo {0} no valido. Tipos permitidos en ese parametro: {1}".format(ext, choices))
        return filename


    parser.add_argument('path_image_from_search', help="Ruta de fichero de imagen donde buscar",
                        type=lambda filename: file_choices(('jpg', 'jpeg', 'png', 'gif'), filename),
                        metavar="image_screenshot.jpg")

    arguments_list = parser.parse_args()

    print(ocr_recognition(path_image_from_search=arguments_list.path_image_from_search))
