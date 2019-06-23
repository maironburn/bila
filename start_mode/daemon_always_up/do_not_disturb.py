import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import win32gui
import time
import win32com.client
import win32con


class AppServerSvc(win32serviceutil.ServiceFramework):
    _svc_name_ = "Do not disturb"
    _svc_display_name_ = "Confidence svc"
    _app_to_care = None
    _hwnd = None

    def __init__(self, args, target_svc):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def window_windows_process(self):
        win32gui.EnumWindows(self.callback, None)

    def callback(self, hwnd, extra=None):
        rect = win32gui.GetWindowRect(hwnd)

        if self._app_to_care in win32gui.GetWindowText(hwnd):
            self.set_values(rect)
            self._hwnd = hwnd

    def set_app_name(self, svc):
        if svc:
            self._app_to_care = svc

    def set_foreground(self, kill_the_enemy=False):

        try:
            foreground_one = win32gui.GetForegroundWindow()
            if foreground_one != self._hwnd:
                if kill_the_enemy:  # @todo quizas una lista blanca de procesos
                    time.sleep(3)
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
            # print("sorry, need it, set_foreground exception -> ".format(e))

    def main(self):
        while True:
            self.set_foreground()
            time.sleep(3)


if __name__ == '__main__':
    AppServerSvc() #@todo, to dig in
    win32serviceutil.HandleCommandLine(AppServerSvc)
