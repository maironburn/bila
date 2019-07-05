import time
import win32api
import win32com.client

def send_keys(text):
    for src, dst in [('{', '['), ('}', ']'), ('(', '{(}'), (')','{)}'), ('+', '{+}'), ('^', '{^}'), (r'%', r'{%}'), ('~', '{~}')]:
        text = text.replace(src, dst)
    shell.SendKeys(text)


time.sleep(5)
shell = win32com.client.Dispatch("WScript.Shell")
#shell.Run("notepad")

shell.AppActivate("Notepad")
send_keys(r"Testing + ^ % ~ ()  +/- {")