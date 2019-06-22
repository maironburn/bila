from os.path import sep
import pyautogui, os
from common_config import TEMP_IMGS, DATASET_IMGS
import cv2
from matplotlib import pyplot as plt
import numpy as np
import pytesseract
from pytesseract import Output
from win32api import GetSystemMetrics


def churrete_masivo():
    taskbar_icon_to_fg = ("{}{}".format(DATASET_IMGS, "tool_bar_icon.jpg"))
    img_rgb = cv2.imread("{}{}".format(TEMP_IMGS, "screenshot.png"), cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(taskbar_icon_to_fg, cv2.IMREAD_GRAYSCALE)

    w, h = template.shape[::-1]
    '''
    # All the 6 methods for comparison in a list
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
               'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
    '''

    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # Specify a threshold
    threshold = 0.8

    # Store the coordinates of matched area in a numpy array
    loc = np.where(res >= threshold)

    # Draw a rectangle around the matched region.
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (128, 128, 128), 2)

    # Show the final image with the matched area.
    cv2.imshow('Detected', img_rgb)
    cv2.waitKey()


def refresh_screenshot():
    im2 = pyautogui.screenshot("{}{}".format(TEMP_IMGS, "screenshot.png"))


def test():
    template = ("{}{}".format(DATASET_IMGS, "tool_bar_icon.jpg"))
    haystack = cv2.imread("{}{}".format(TEMP_IMGS, "screenshot.png"), cv2.IMREAD_COLOR)
    needle = cv2.imread(template, cv2.IMREAD_COLOR)

    w, h, _ = needle.shape

    output = needle.copy()
    cv2.namedWindow('output', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('output', 1024, 800)
    roi = needle[:, 50:]

    cv2.imshow("output", roi)
    # cv2.imshow("needle", needle)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return


def testing_img_recongnition_pyautogui():
    directory = ("{}{}".format(DATASET_IMGS, "windows.py"))
    print("directorio de busqueda: {}".format(directory))
    for filename in os.listdir(directory):
        if filename.endswith(".asm") or filename.endswith(".py"):
            # print(os.path.join(directory, filename))
            continue
        else:
            template = ("{}{}{}{}".format(DATASET_IMGS, "windows.py", sep, filename))
            print("buscando template: {}".format(filename))
            found = pyautogui.locateOnScreen(template)
            if found:
                left, top, width, height = pyautogui.locateOnScreen(template)
                print("left: {} , top: {}, width: {}, height: {}".format(left, top, width, height))
            else:
                print("template: {} no encontrado".format(template))


def which_window_am_i():
    return "main_window"


def text_recognition():

    try:
        image_file=  ("{}{}".format(TEMP_IMGS, "screenshot.png"))
        img = cv2.imread(image_file)
        d = pytesseract.image_to_data(img, output_type=Output.DICT)
        n_boxes = len(d['level'])
        modelos = [i for i, x in enumerate(d['text']) if x == "Modelo"]
        for i in range(n_boxes):
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('img', img)
        cv2.waitKey(0)

    except Exception as e:
        print ("text_recognition: {}".format(e))


def text_recognition2():
    try:

        image_file = ("{}{}".format(TEMP_IMGS, "screenshot.png"))
        img = cv2.imread(image_file)
        h, w, _ = img.shape  # assumes color image

        # run tesseract, returning the bounding boxes
        boxes = pytesseract.image_to_boxes(img)  # also include any config options you use

        # draw the bounding boxes on the image
        for b in boxes.splitlines():
            b = b.split(' ')
            img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

        # show annotated image and wait for keypress
        cv2.imshow(image_file, img)
        cv2.waitKey(0)
    except Exception as e:
        print ("text_recognition: {}".format(e))


if __name__ == '__main__':
    # start app
    refresh_screenshot()
    #text_recognition()
    start_window = which_window_am_i()

    image_window = "Source Image"
    result_window = "Result window"
    directory = ("{}{}".format(DATASET_IMGS,start_window))
    print("directorio de busqueda: {}".format(directory))
    img_path = ("{}{}".format(TEMP_IMGS, "screenshot.png"))

    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    img_display = img.copy()

    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            continue
        else:
            template = ("{}{}{}{}".format(DATASET_IMGS, "windows.py", sep, filename))
            print("buscando template: {}".format(filename))
            templ = cv2.imread(template, cv2.IMREAD_COLOR)
            img_display = img.copy()

            result = cv2.matchTemplate(img, templ, cv2.TM_CCORR_NORMED)
            cv2.normalize(result, result, 0, 1, cv2.NORM_MINMAX, -1)
            _minVal, _maxVal, minLoc, maxLoc = cv2.minMaxLoc(result, None)
            matchLoc = maxLoc
            '''
            beatiful visual testing purposes
            
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

            pyautogui.dragTo(x_center, y_center, duration=0)
            # pyautogui.click()

            '''
            beatiful visual testing purposes
            
            cv2.circle(img_display, center, 5, (0, 255, 0), -1)
            cv2.imshow(image_window, img_display)

            cv2.waitKey(0)
            cv2.destroyAllWindows()
            '''
    # plt.switch_backend('agg')
    # test()

    # churrete_masivo()
