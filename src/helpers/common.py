from src.models import elemento
from common_config import TEMP_IMGS
import pyautogui

'''
extract name until first _ cause it defines class type
'''


def get_type_from_filename(filename):
    return filename.split('_')[0].capitalize()


'''element name without extension neither type'''


def get_element_name_from_filename(filename):
    return filename[0:filename.index('.')][filename.index('_') + 1:]


'''instantiating attending to element_type (inferred by the filename first _  )'''


def dinamic_instance_elements(element_type, init_values):
    try:
         # getattr(module, class_name)
        element_type = getattr(elemento, element_type)
        return element_type(init_values)

    except Exception as e:
        pass
    return None

def capture_screen():
    pyautogui.screenshot("{}{}".format(TEMP_IMGS, "screenshot.png"))

