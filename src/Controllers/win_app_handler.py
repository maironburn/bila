import win32gui, win32con
from win32api import GetSystemMetrics
from common_config import APP_NAME
from time import sleep
from loggin.AppLogger import AppLogger

'''
class to handle app window and avoid intromisions
'''


class WinAppHandler(object):
    _hwnd = None
    _screen_w = None
    _screen_h = None
    _location_x = None
    _location_y = None
    _width = None
    _height = None

    def __init__(self):
        self.logger = AppLogger.create_log()
        win32gui.EnumWindows(self.callback, None)

    def callback(self, hwnd, extra):
        rect = win32gui.GetWindowRect(hwnd)

        if APP_NAME in win32gui.GetWindowText(hwnd):
            self.set_values(rect)
            self._hwnd = hwnd

    def set_values(self, rect):

        self._screen_w = GetSystemMetrics(0)
        self._screen_h = GetSystemMetrics(1)
        self._location_x = rect[0]
        self._location_y = rect[1]
        self._width = rect[2] - self._location_x
        self._height = rect[3] - self._location_y

    def set_foreground(self, kill_the_enemy=False):

        foreground_one = win32gui.GetForegroundWindow()
        if foreground_one != self._hwnd:
            self.logger.info("checking foreground: {}".format("Hay un Usurpador, un vampiro digital"))
            self.maximize_window()
            win32gui.SetForegroundWindow(self._hwnd)
            win32gui.SetActiveWindow(self._hwnd)
            if kill_the_enemy:
                sleep(3)
                win32gui.PostMessage(foreground_one, win32con.WM_CLOSE, 0, 0)

    def maximize_window(self):
        win32gui.ShowWindow(self._hwnd, win32con.SW_MAXIMIZE)

    def log_screen_features(self):
        self.logger.info("Width ={}, Height ={}".format(self._screen_w, self._screen_h))
        self.logger.info("Location = ({},{})".format(self._location_x, self._location_y))
        self.logger.info("Size (h,w) = ({},{})".format(self._height, self._width))

    @property
    def get_h_w(self):
        return "{}x{}".format(self._width, self._height)

    @property
    def handler(self):
        if self._hwnd:
            return self._hwnd


if __name__ == '__main__':
    win_hwnd = WinAppHandler()
    win_hwnd.set_foreground(False)
