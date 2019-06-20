import os
import time
import win32gui
import win32ui
from ctypes import windll
from PIL import Image

from common_config import OUTPUT_FOLDER
from settings.settings import window_names, capture_image_name


def extract_window_screenshot():
    for window_name in window_names:
        hwnd = win32gui.FindWindow(None, window_name)
        if hwnd:
            break
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
            image.save(os.path.join(OUTPUT_FOLDER, capture_image_name))

        return os.path.join(OUTPUT_FOLDER, capture_image_name)
    else:
        raise Exception("Ventana no encontrada")


if __name__ == '__main__':
    time.sleep(5)
    extract_window_screenshot()
