import os
import time
import win32gui, win32con
import win32api
import win32ui
from ctypes import windll
from PIL import Image
from common_config import TEMP_IMGS


class Interactive_Manager(object):
    dict_windows = {'main': 'Plataforma de programas de ayuda',
                    'error_validacion': 'BIZKAIKO FORU ALDUNDIA - DIPUTACIÓN FORAL DE BIZKAIA'
                    }

    not_welcome = ['BFA / DFB']  # splash windows

    running_gui_app = {}

    legacy_app = None
    intruder = None

    def __init__(self, kw=None):
        # self.legacy_app = kw.get('legacy', None)
        self.window_features()

    def window_features(self):
        win32gui.EnumWindows(self.callback, None)

    def callback(self, hwnd, extra=None):
        rect = win32gui.GetWindowRect(hwnd)
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != '':
            ''' creates dict window_app: handler '''
            self.running_gui_app.update({"{}".format(win32gui.GetWindowText(hwnd)): hwnd})
            print("{} -> {}".format(win32gui.GetWindowText(hwnd), win32gui.GetClassName(hwnd)))
            #if self.dict_windows['main'] in win32gui.GetWindowText(hwnd):
            if 'texto a escribir' in win32gui.GetWindowText(hwnd):
                print("{}- > {}".format(self.dict_windows['main'], hwnd))
                self.legacy_app = hwnd

            # print("{} -> {}".format(win32gui.GetWindow(hwnd), win32gui.GetClassName(hwnd)))

    def kill_splash(self):
        for k, v in self.running_gui_app.items():
            if k in self.not_welcome:
                win32gui.PostMessage(v, win32con.WM_CLOSE, 0, 0)

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

    def move_mouse(self, x, y):

        win32api.SetCursorPos((x, y))
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

    # def send_input_hax(self, msg):
    #
    #     for c in msg:
    #         win32api.PostMessage (self.legacy_app, win32con.WM_KEYDOWN, ord(c), 0)
    #         win32api.PostMessage(self.legacy_app, win32con.WM_CHAR, ord(c), 0)
    #         win32api.PostMessage(self.legacy_app, win32con.WM_KEYUP, ord(c), 0)


    def send_input_hax(self, msg):

        for c in msg:
            win32api.KeyPress(c)



    def SetText(self,  text):
        textformat = win32con.DT_LEFT | win32con.DT_TOP
        hDC, paintStruct = win32gui.BeginPaint(self.legacy_app)

        rect = win32gui.GetClientRect(self.legacy_app)
        win32gui.DrawText(
            hDC,
            'Hello send by Python via Win32!',
            -1,
            rect,
            win32con.DT_SINGLELINE | win32con.DT_CENTER | win32con.DT_VCENTER)

        win32gui.EndPaint(self.legacy_app, paintStruct)
        #win32api.SendMessage(self.legacy_app, win32con.WM_SETTEXT, None, text)


if __name__ == '__main__':
    # time.sleep(5)
    # C:\BILA\BILA\N4BL.exe#
    wf = Interactive_Manager()
    wf.kill_splash()
    time.sleep(5)
    print("q voyyy")
    #wf.move_mouse(500, 500)
    wf.send_input_hax('texto a escribirtexto a escribirtexto a escribirtexto a escribir')
    #wf.SetText('texto a escribir')
    # extract_window_screenshot(dict_windows['main'])
