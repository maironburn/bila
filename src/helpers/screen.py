from win32api import GetSystemMetrics
from common_config import TEMP_IMGS
import pyautogui


def screen_resolution():
    screen_w = GetSystemMetrics(0)
    screen_h = GetSystemMetrics(1)

    return "{}x{}".format(screen_w, screen_h)


def capture_screen(name="screenshot.png"):
    pyautogui.screenshot("{}{}".format(TEMP_IMGS, name))




if __name__ == '__main__':
    print("{}".format(screen_resolution()))
