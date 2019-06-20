import argparse
import os
from src.extract_window import extract_window_screenshot

def area_recognition(path_image_to_search=None, path_image_from_search=None, object_name_to_search=None):
    if not path_image_from_search:
        path_image_from_search = extract_window_screenshot()

    if path_image_to_search:
        # TODO comportamiento normal, de busqueda de imagen
        if object_name_to_search:
            pass  # TODO estorageamos el nombre de imagen para ir creando el dataset

    else:
        if object_name_to_search:
            if "dataset_created_and_trained" == "blaa":
                pass  # TODO aqui se comprueba si hay dataset entrenado y creado para usar AI para reconocimiento de imagen pasando nombre de objeto
            else:
                raise Exception(
                    "Es necesario recibir imagen a buscar, o en su defecto nombre de objeto a buscar, si hay dataset creado y entrenado")
        else:
            raise Exception("Es necesario pasar una imagen a buscar o un nombre de objeto a buscar")


if __name__ == '__main__':
    print("Interfaz de reconocimiento de posicion de imagen \n")
    parser = argparse.ArgumentParser(description='Interfaz de reconocimiento de posicion de imagen')


    def file_choices(choices, filename):
        ext = os.path.splitext(filename)[1][1:]
        if ext not in choices or not ext:
            parser.error("Tipo de archivo {0} no valido. Tipos permitidos en ese parametro: {1}".format(ext, choices))
        return filename


    parser.add_argument('--path_image_to_search', help="Ruta del fichero de imagen a buscar",
                        type=lambda filename: file_choices(('jpg', 'jpeg', 'png', 'gif'), filename),
                        metavar="image.jpg")
    parser.add_argument('--path_image_from_search', help="Ruta de fichero de imagen donde buscar",
                        type=lambda filename: file_choices(('jpg', 'jpeg', 'png', 'gif'), filename),
                        metavar="image_screenshot.jpg")
    parser.add_argument('--object_name_to_search', help="Nombre de objeto a buscar",
                        metavar="close_button")

    arguments_list = parser.parse_args()

    print(area_recognition(path_image_to_search=arguments_list.path_image_to_search,
                           path_image_from_search=arguments_list.path_image_from_search,
                           object_name_to_search=arguments_list.object_name_to_search))
