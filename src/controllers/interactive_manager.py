import os
import time
import win32gui
import win32ui
from ctypes import windll
from PIL import Image
from common_config import TEMP_IMGS


class Interactive_Manager(object):

    dict_windows = {'main': 'Plataforma de programas de ayuda',
                    'error_validacion': 'BIZKAIKO FORU ALDUNDIA - DIPUTACIÓN FORAL DE BIZKAIA'
                    }

    def __init__(self):
        pass

    def window_features(self):
        win32gui.EnumWindows(self.callback, None)

    def callback(self, hwnd, extra=None):
        rect = win32gui.GetWindowRect(hwnd)
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != '':
            print("{}".format(win32gui.GetWindowText(hwnd)))

    def extract_window_screenshot(self, window_name):
        windows = []
        # for window_name in '':
        hwnd = win32gui.FindWindow(None, window_name)

        if hwnd:
            # Change the line below depending on whether you want the whole window
            # or just the client area.
            # left, top, right, bot = win32gui.GetClientRect(hwnd)
            left, top, right, bot = win32gui.GetWindowRect(hwnd)
            w = right - left
            h = bot - top

            hwndDC = win32gui.GetWindowDC(hwnd)
            mfcDC = win32ui.CreateDCFromHandle(hwndDC)
            saveDC = mfcDC.CreateCompatibleDC()

            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

            saveDC.SelectObject(saveBitMap)

            # Change the line below depending on whether you want the whole window
            # or just the client area.
            # result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
            result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)

            bmpinfo = saveBitMap.GetInfo()
            bmpstr = saveBitMap.GetBitmapBits(True)

            image = Image.frombuffer(
                'RGB',
                (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                bmpstr, 'raw', 'BGRX', 0, 1)

            win32gui.DeleteObject(saveBitMap.GetHandle())
            saveDC.DeleteDC()
            mfcDC.DeleteDC()
            win32gui.ReleaseDC(hwnd, hwndDC)

            if result == 1:
                image.save("{}{}".format(TEMP_IMGS, 'testing_capture.png'))

        else:
            raise Exception("Ventana no encontrada")


if __name__ == '__main__':
    time.sleep(5)
    # window_features()
    # extract_window_screenshot(dict_windows['main'])
