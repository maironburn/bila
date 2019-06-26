from os.path import sep
import pyautogui, os
from common_config import TEMP_IMGS, DATASET_IMGS
import cv2


def getElementCoords(haystack, needle):

    img = cv2.imread(haystack, cv2.IMREAD_COLOR)
    img_display = img.copy()
    templ = cv2.imread(needle, cv2.IMREAD_COLOR)
    result = cv2.matchTemplate(img, templ, cv2.TM_CCORR_NORMED)
    cv2.normalize(result, result, 0, 1, cv2.NORM_MINMAX, -1)
    _minVal, _maxVal, minLoc, maxLoc = cv2.minMaxLoc(result, None)
    matchLoc = maxLoc
    h, w, _ = templ.shape

    center = (int((matchLoc[0] + w / 2)), int((matchLoc[1] + templ.shape[0]) - h / 2))
    x_center = int(matchLoc[0] + w / 2)
    y_center = int((matchLoc[1] + templ.shape[0]) - h / 2)

    return x_center, y_center



if __name__ == '__main__':
    # start app
    #refresh_screenshot()
    # text_recognition()
    #start_window = which_window_am_i()

    image_window = "Source Image"
    result_window = "Result window"
    directory = ("{}{}".format(DATASET_IMGS, 'main_window'))
    print("directorio de busqueda: {}".format(directory))
    img_path = ("{}{}".format(TEMP_IMGS, "declarantes_screenshot.png"))

    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    img_display = img.copy()

    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            continue
        else:
            template = ("{}{}{}{}".format(DATASET_IMGS, "main_window", sep, filename))
            print("buscando template: {}".format(filename))
            templ = cv2.imread(template, cv2.IMREAD_COLOR)
            img_display = img.copy()

            result = cv2.matchTemplate(img, templ, cv2.TM_CCORR_NORMED)
            cv2.normalize(result, result, 0, 1, cv2.NORM_MINMAX, -1)
            _minVal, _maxVal, minLoc, maxLoc = cv2.minMaxLoc(result, None)
            matchLoc = maxLoc
            '''
            beautiful visual testing purposes

            #cv2.namedWindow(image_window, cv2.WINDOW_AUTOSIZE)
            #font = cv2.FONT_HERSHEY_CLoc[0] + templ.shape[1] - 150, matchLoc[1] + templ.shape[0] - 30),
            #           font, 1, (0, 255, 0), 1, cv2.LINE_AA)
            #cv2.rectangle(img_display, matchLoc, (matchLoc[0] + templ.shape[1], matchLoc[1] + templ.shape[0]),
            #              (0, 0, 0), 2, 8, 0)
            '''
            h, w, _ = templ.shape
            print("h:{}, w:{}".format(h, w))

            center = (int((matchLoc[0] + w / 2)), int((matchLoc[1] + templ.shape[0]) - h / 2))
            x_center = int(matchLoc[0] + w / 2)
            # text = '_'.join(filename.split('_')[1:]).split('.')[0]
            # cv2.putText(img_display, text, (match
            y_center = int((matchLoc[1] + templ.shape[0]) - h / 2)

            pyautogui.dragTo(x_center, y_center, duration=1)
            # pyautogui.click()

            '''
            beautiful visual testing purposes

            cv2.circle(img_display, center, 5, (0, 255, 0), -1)
            cv2.imshow(image_window, img_display)

            cv2.waitKey(0)
            cv2.destroyAllWindows()
            '''
    # plt.switch_backend('agg')
    # test()

    # churrete_masivo()
