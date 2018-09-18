import win32api
import win32con
import time
from const import VK_CODE


def press_key(key):
    win32api.keybd_event(VK_CODE[key], 0, 0, 0)
    time.sleep(.05)
    win32api.keybd_event(VK_CODE[key], 0, win32con.KEYEVENTF_KEYUP, 0)