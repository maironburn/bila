
from os.path import sep
import pyautogui, os
from common_config import TEMP_IMGS,DATASET_IMGS
import cv2
from matplotlib import pyplot as plt
import numpy as np
from win32api import GetSystemMetrics



def churrete_masivo():

    taskbar_icon_to_fg = ("{}{}".format(DATASET_IMGS, "tool_bar_icon.jpg"))
    img_rgb = cv2.imread("{}{}".format(TEMP_IMGS,"declarantes_screenshot.png"), cv2.IMREAD_GRAYSCALE)
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
    im2 = pyautogui.screenshot("{}{}".format(TEMP_IMGS,"declarantes_screenshot.png"))


def singleton_matching():

    template  = ("{}{}".format(DATASET_IMGS, "tool_bar_icon.jpg"))
    haystack = cv2.imread("{}{}".format(TEMP_IMGS,"declarantes_screenshot.png"), cv2.IMREAD_GRAYSCALE)
    needle = cv2.imread(template, cv2.IMREAD_GRAYSCALE)

    w, h = needle.shape

    match_method=cv2.TM_CCOEFF_NORMED
    # Perform match operations.
    match = cv2.matchTemplate(haystack, needle, cv2.TM_CCOEFF_NORMED)
    minVal, maxVal, minLoc, maxLoc = cv2.MinMaxLoc(match)
    # threshold

    '''
    if not ocr:
        cv2.imshow('Template Found', haystack)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    '''

    output = haystack.copy()
    cv2.imshow("cropped", output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return


def click(target=None):

    try:
        if target is None:
            taskbar_icon_to_fg = ("{}{}".format(DATASET_IMGS, "tool_bar_icon.jpg"))
            target_coords= pyautogui.locateOnScreen(taskbar_icon_to_fg)
            if target_coords and len(target_coords):
                avg_point_to_click=pyautogui.center(target_coords)
                coord_x, coord_y =avg_point_to_click
                pyautogui.click(coord_x, coord_y)

    except Exception as e:
        print("{}".format(e))



if __name__ == '__main__':
    print("Width =", GetSystemMetrics(0))
    print("Height =", GetSystemMetrics(1))

    refresh_screenshot()

    plt.switch_backend('agg')
    singleton_matching()

    #churrete_masivo()