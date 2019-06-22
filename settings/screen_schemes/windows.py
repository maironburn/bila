import os.path
from common_config import TEMP_IMGS, DATASET_IMGS

main_window = {
    "nombre": "main",
    "parent": None,
    "img_folder": "{}{}".format(DATASET_IMGS, "main_window"),
    "dict_elementos": {'declarantes': '', 'modelo_declaracion': '',
                       'presentadores': '', 'copia_seguridad': '',
                       'intalacion_actualizacion': '',
                       'configurar_plataforma': '', 'utilidades': '',
                       'ayuda': '', 'salir': ''}
}
