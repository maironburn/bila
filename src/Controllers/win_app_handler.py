import win32gui, win32con
from win32api import GetSystemMetrics
from common_config import APP_NAME
from time import sleep
import  win32com.client

class WinAppHandler(object):
    _hwnd = None
    _location_x = None
    _location_y = None
    _width = None
    _height = None

    def __init__(self):
        win32gui.EnumWindows(self.callback, None)

    def callback(self, hwnd, extra):
        rect = win32gui.GetWindowRect(hwnd)

        if APP_NAME in win32gui.GetWindowText(hwnd):
            self.set_values(rect)
            self._hwnd = hwnd

    def set_values(self, rect):
        self._location_x = rect[0]
        self._location_y = rect[1]
        self._width = rect[2] - self._location_x
        self._height = rect[3] - self._location_y

        print("\tLocation: (%d, %d)" % (self._location_x, self._location_y))
        print("\t    Size: (%d, %d)" % (self._width, self._height))

    def set_foreground(self, kill_the_enemy=False):

        foreground_one = win32gui.GetForegroundWindow()
        if foreground_one != self._hwnd:
            self.maximize_window()
            win32gui.SetForegroundWindow(self._hwnd)
            win32gui.SetActiveWindow(self._hwnd)
            if kill_the_enemy:
                sleep(3)
                win32gui.PostMessage(foreground_one, win32con.WM_CLOSE, 0, 0)


    def maximize_window(self):
        win32gui.ShowWindow(self._hwnd, win32con.SW_MAXIMIZE)


if __name__ == '__main__':
    print("Width =", GetSystemMetrics(0))
    print("Height =", GetSystemMetrics(1))

    win_hwnd = WinAppHandler()
    win_hwnd.set_foreground(True)

