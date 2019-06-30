import os.path
from common_config import TEMP_IMGS, DATASET_IMGS

main = {
    "_name": "main",
    "_parent": None,
    "_img_folder": "{}{}".format(DATASET_IMGS, "main_window"),
    "_dict_elements": {'declarantes': '', 'modelo_declaracion': '',
                       'presentadores': '', 'copia_seguridad': '',
                       'instalacion_actualizacion': '',
                       'configurar_plataforma': '', 'utilidades': '',
                       'ayuda': '', 'exit': ''}
}

declarantes = {
    "_name": "declarantes",
    "_parent": "main",
    "_img_folder": "{}{}{}".format(main['_img_folder'], os.path.sep, "declarantes"),
    "_dict_elements": {'busqueda_nombre_rz': '', 'quitar_filtro': '',
                       # ...
                       'nuevo_declarante': '',
                       'salir': ''}
}

nuevo_declarante = {
    "_name": "nuevo_declarante",
    "_parent": "declarantes",
    "_img_folder": "{}{}{}".format(declarantes['_img_folder'], os.path.sep, 'nuevo_declarante'),
    "_dict_elements": {}
}

telf_mail = {
    "_name": "telf_mail",
    "_parent": "nuevo_declarante",
    "_img_folder": "{}{}{}".format(nuevo_declarante['_img_folder'], os.path.sep, 'telf_mail'),
    "_dict_elements": {}
}