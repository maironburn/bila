import win32gui, win32con

from common_config import APP_NAME
from time import sleep
from loggin.app_logger import AppLogger
import win32com.client
from common_config import TIME_SLEEP, KILL_THE_ENEMY, TIME_WAIT_AFTER_KILLING
'''
class to handle app window, control running status, size and avoid intromisions
'''


class WinAppHandler(object):
    _hwnd = None
    _location_x = None
    _location_y = None
    _width = None
    _height = None
    _logger = None

    def __init__(self, logger=None):
        self._logger = AppLogger.create_log() if not logger else logger
        self.window_features()

    def window_features(self):
        win32gui.EnumWindows(self.callback, None)

    def callback(self, hwnd, extra=None):
        rect = win32gui.GetWindowRect(hwnd)
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != '':
            if APP_NAME in win32gui.GetWindowText(hwnd):
                self.set_values(rect)
                self._hwnd = hwnd
                self.log_screen_features()

    def set_values(self, rect):

        self._location_x = rect[0]
        self._location_y = rect[1]
        self._width = rect[2] - self._location_x
        self._height = rect[3] - self._location_y

    def daemon_dont_disturb_please(self):

        while self._hwnd:
            try:
                self.set_foreground()
                # @todo, too much killer..too much Dexter
                self._logger.info("daemon_dont_disturb_please, modo Killer")
                sleep(TIME_SLEEP)
            except Exception as e:
                pass

    def set_foreground(self):

        try:
            foreground_one = win32gui.GetForegroundWindow()
            if foreground_one != self._hwnd:
                if KILL_THE_ENEMY:  # @todo quizas una lista blanca de procesos
                    sleep(TIME_WAIT_AFTER_KILLING)
                    win32gui.PostMessage(foreground_one, win32con.WM_CLOSE, 0, 0)

                self._logger.info("checking foreground: {}".format("Hay un Usurpador, un vampiro digital"))
                self.maximize_window()
                shell = win32com.client.Dispatch("WScript.Shell")
                shell.SendKeys('%')
                win32gui.SetForegroundWindow(self._hwnd)
                win32gui.SetActiveWindow(self._hwnd)
                win32gui.SetFocus(self._hwnd)
                self.window_features()  # refresh dims

        except Exception as e:
            self._logger.error("set_foreground exception -> ".format(e))

    def maximize_window(self):
        win32gui.ShowWindow(self._hwnd, win32con.SW_MAXIMIZE)

    def log_screen_features(self):

        self._logger.info("Location = ({},{})".format(self._location_x, self._location_y))
        self._logger.info("app window size (h,w) = ({},{})".format(self._height, self._width))

    @property
    def get_h_w(self):
        return "{}x{}".format(self._width, self._height)

    @property
    def handler(self):
        if self._hwnd:
            return self._hwnd


if __name__ == '__main__':
    win_hwnd = WinAppHandler()
    win_hwnd.set_foreground()
