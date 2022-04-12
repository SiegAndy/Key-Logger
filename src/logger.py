from typing import List
import win32gui, win32process, win32con, win32api
from time import sleep


class windowHandler:
    
    def __init__(self, target_window: str = None, target_process_id = None, keystrokes: List = None) -> None:
        self.windows = []
        self.keystrokes = keystrokes
        self.working_hwndMain = -1
        self.working_hwndChild = -1
        self.working_pid = -1
        self.working_threadid = -1


    def select_target_window(self):
        
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != '':
                self.windows.append((hwnd, win32gui.GetWindowText(hwnd), win32gui.GetClassName(hwnd)))
                print (hex(hwnd), win32gui.GetWindowText(hwnd), win32gui.GetClassName(hwnd))

        # empty previous windows
        self.windows = []
        win32gui.EnumWindows(winEnumHandler, None)

        return self.windows


    def get_window_info(self, title):
        hwndMain = win32gui.FindWindow(None, title)
        if hwndMain == 0:
            raise ValueError("Unable to find target windows, the window could be un-saved or not exist.\nPlease enter valid title for the target window!")
        hwndChild = win32gui.GetWindow(hwndMain, win32con.GW_CHILD)

        threadid, pid = win32process.GetWindowThreadProcessId(hwndMain)

        self.working_hwndMain = hwndMain
        self.working_hwndChild = hwndChild
        self.working_pid = pid
        self.working_threadid = threadid

        return hwndMain, hwndChild, pid, threadid


    def execute(self, keystrokes: List = None, number_of_time: int = None, time_interval: int = None):
        """
        @param
        keystrokes: a list of keystroke for execution
        number_of_time: the number of time for execute the keystroke combination
        time_interval: the time interval that keystroke will execute
        """
        hwndMain = self.working_hwndMain

        while True:
            temp = win32api.PostMessage(hwndMain, win32con.WM_CHAR, ord('A'), 0)
            temp = win32api.PostMessage(hwndMain, win32con.WM_CHAR, ord('W'), 0)
            temp = win32api.PostMessage(hwndMain, win32con.WM_CHAR, ord('s'), 0)
            temp = win32api.PostMessage(hwndMain, win32con.WM_CHAR, ord('d'), 0)
            box_title = "Test Message Send"
            # win32gui.MessageBox(hwndMain, "Hello", "Test Message Send", win32con.MB_OK)
            index=2
            win32gui.SendMessage(hwndMain,win32con.CB_SETCURSEL,index,0)

            #trigger event
            win32gui.SendMessage(hwndMain, win32con.WM_LBUTTONDOWN, 0, 0)
            win32gui.SendMessage(hwndMain, win32con.WM_LBUTTONUP, 0, 0)
            win32gui.SendMessage(hwndMain, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.SendMessage(hwndMain, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
            win32gui.SendMessage(hwndMain, win32con.CBN_SELCHANGE)
            win32gui.SendMessage(hwndMain, win32con.CBN_SELENDOK)
            sleep(1)



process_name = r"""E:\Extra\Key-Logger\test\test.txt - Sublime Text (UNREGISTERED)"""
instance = windowHandler()
result = instance.select_target_window()
hwndMain, hwndChild, threadid, pid = instance.get_window_info(result[2][1]) 
# print(hwndMain, hwndChild, threadid, pid)
instance.execute()



