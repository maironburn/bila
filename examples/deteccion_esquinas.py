
from os.path import sep
import pyautogui, os
from common_config import TEMP_IMGS,DATASET_IMGS
import cv2
from matplotlib import pyplot as plt
import numpy as np
from win32api import GetSystemMetrics

def refresh_screenshot():
    im2 = pyautogui.screenshot("{}{}".format(TEMP_IMGS,"screenshot.png"))


def detectar_esquinas():

    haystack = cv2.imread("{}{}".format(DATASET_IMGS,"tool_bar_icon.jpg"), cv2.IMREAD_COLOR)
    gray_haystack = cv2.cvtColor(haystack, cv2.COLOR_BGR2GRAY)

    gray = np.float32(gray_haystack)
    dst = cv2.cornerHarris(gray, 2, 3, 0.04)

    height, width = dst.shape
    color = (0, 255, 0)

    for y in range(0, height):
        for x in range(0, width):
            if dst.item(y, x) > 0.01 * dst.max():
                cv2.circle(haystack, (x, y), 3, color, cv2.FILLED, cv2.LINE_AA)

    cv2.imshow('Harris Result', dst)
    cv2.imshow('Harris Corner', haystack)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return


def threshold():
    src = cv2.imread("{}{}".format(TEMP_IMGS,"screenshot.png"))
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 3)

    t, dst = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)

    _, contours, _ = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        area = cv2.contourArea(c)
        if area > 1000 and area < 10000:
            cv2.drawContours(src, [c], 0, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow('contornos', src)
    cv2.imshow('umbral', dst)

    cv2.waitKey(0)

if __name__ == '__main__':
    print("Width =", GetSystemMetrics(0))
    print("Height =", GetSystemMetrics(1))
    plt.switch_backend('agg')
    #refresh_screenshot()
    threshold()

    #churrete_masivo()