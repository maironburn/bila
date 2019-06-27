from win32api import GetSystemMetrics
from common_config import TEMP_IMGS, SCREEN_BANNERS
import pyautogui
import pytesseract as pytesseract
from PIL import Image
from markdown.extensions.toc import slugify
from common_config import TEMP_IMGS
import os
import cv2

dictio_screentext_identificative = {

    'plataforma de programas de ayuda': 'main',
    'lista de declarantes': 'declarantes',
    'datos del declarante': 'nuevo_declarante',
    'cambiar NIF': 'modificar_nif'
                   ''' ...'''
}


def screen_resolution():
    screen_w = GetSystemMetrics(0)
    screen_h = GetSystemMetrics(1)

    return "{}x{}".format(screen_w, screen_h)


def tesseract_data_to_string(string_data, update_with_coord=True):
    data_list = []
    for line_num, line in enumerate(string_data.split("\n")):
        line_dict = {}
        if line_num == 0:
            headers = line.split("\t")
        else:
            for attrib_num, value in enumerate(line.split("\t")):
                line_dict.update({headers[attrib_num]: value})
            if line_dict.get("text") and line_dict.get("text").strip():
                if update_with_coord:
                    text = line_dict.get("text").strip()
                data_list.append(text)
    return ' '.join([i.lower() for i in data_list])


def ocr_screen_recognition(src_img=None, txt_needle=None):
    haystack_text = pytesseract.image_to_data(Image.open('%s' % (src_img,)))
    for k, v in dictio_screentext_identificative.items():
        if k in haystack_text.lower():
            return dictio_screentext_identificative[k]

    return None


def ocr_screen_recognition_kk(src_img=None, txt_needle=None):
    result_to_data = pytesseract.image_to_string(Image.open(src_img))  # ? vasco
    list_data = tesseract_data_to_string(result_to_data)

    for k, v in dictio_screentext_identificative.items():
        if k in list_data:
            return dictio_screentext_identificative[k]

    return None


def getElementCoords(haystack, needle):
    img = cv2.imread(haystack, cv2.IMREAD_COLOR)
    img_display = img.copy()
    templ = cv2.imread(needle, cv2.IMREAD_COLOR)
    result = cv2.matchTemplate(img, templ, cv2.TM_CCORR_NORMED)
    cv2.normalize(result, result, 0, 1, cv2.NORM_MINMAX, -1)
    _minVal, _maxVal, minLoc, maxLoc = cv2.minMaxLoc(result, None)
    matchLoc = maxLoc
    print("{} ->  minVal:  {}, maxVal:   {}".format(needle, _minVal, _maxVal))

    return _minVal
    '''
    h, w, _ = templ.shape

    center = (int((matchLoc[0] + w / 2)), int((matchLoc[1] + templ.shape[0]) - h / 2))
    x_center = int(matchLoc[0] + w / 2)
    y_center = int((matchLoc[1] + templ.shape[0]) - h / 2)

    return x_center, y_center
    '''


def capture_screen(name="screenshot"):
    pyautogui.screenshot("{}{}.png".format(TEMP_IMGS, name))
    print("captured windows: {}".format(name))


if __name__ == '__main__':
    # print("{}".format(screen_resolution()))
    capture_screen()
    # src_img = ("{}{}".format(TEMP_IMGS, "screenshot.png"))
    haystack = ("{}{}".format(TEMP_IMGS, "screenshot.png"))
    samples = []
    dict_sample = {}
    for filename in [x for x in os.listdir(SCREEN_BANNERS)]:
        needle = "{}{}{}".format(SCREEN_BANNERS, os.path.sep, filename)
        dict_sample.update({filename: getElementCoords(haystack, needle)})

    target = min(dict_sample.values())
    for k, v in dict_sample.items():
        if target == v:
            print("target : {}".format(k))

    print("end")

'''
#needle = "{}{}{}".format(SCREEN_SNAP, os.path.sep, 'nuevo_declarante.png')

needle = ("{}{}".format(TEMP_IMGS, "screenshot.png"))
print(getElementCoords(needle))
'''
