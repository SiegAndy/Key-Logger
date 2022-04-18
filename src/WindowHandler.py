import win32gui, win32process, win32con, win32api
from typing import List
from Pattern import Pattern


class WindowHandler:
    def __init__(self, target_window: str = None, target_process_id=None) -> None:
        self.windows = []
        if target_window is not None:
            self.get_all_windows()
            self.find_designated_window(target_string=target_window)
        else:
            self.working_hwndMain = -1
            self.working_hwndChild = -1
            self.working_pid = -1
            self.working_threadid = -1

    def get_all_windows(self):
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != "":
                self.windows.append(
                    (hwnd, win32gui.GetWindowText(hwnd), win32gui.GetClassName(hwnd))
                )
                # print(
                #     hex(hwnd), win32gui.GetWindowText(hwnd), win32gui.GetClassName(hwnd)
                # )

        # empty previous windows
        self.windows = []
        win32gui.EnumWindows(winEnumHandler, None)

        return self.windows

    def find_designated_window(self, target_string: str, windows: List = None):

        target_string = target_string.lower()
        if windows is None:
            windows = self.windows

        result_window = None

        for window in windows:
            curr_hwnd, curr_text, curr_class = window
            curr_text = curr_text.lower()
            if target_string in curr_text:
                if result_window is not None:
                    raise ValueError(
                        "More than one windows with searched string, please be specific!"
                    )
                result_window = window

        if result_window is None:
            raise ValueError(
                f"Unable to find designated Window with '{target_string}'.\nPlease make sure input string is in its title!"
            )
        self.working_hwndMain = result_window[0]

        return result_window

    def get_window_info(self, title):
        hwndMain = win32gui.FindWindow(None, title)
        if hwndMain == 0:
            raise ValueError(
                "Unable to find target windows, the window could be un-saved or not exist.\nPlease enter valid title for the target window!"
            )
        hwndChild = win32gui.GetWindow(hwndMain, win32con.GW_CHILD)

        threadid, pid = win32process.GetWindowThreadProcessId(hwndMain)

        self.working_hwndMain = hwndMain
        self.working_hwndChild = hwndChild
        self.working_pid = pid
        self.working_threadid = threadid

        return hwndMain, hwndChild, pid, threadid

    def execute(self, pattern: Pattern):
        """
        @param
        keystrokes: a list of keystroke for execution
        number_of_time: the number of time for execute the keystroke combination
        time_interval: the time interval that keystroke will execute
        """

        def send_box():
            box_msg = "Hello"
            box_title = "Test Message Send"
            win32gui.MessageBox(hwndMain, box_msg, box_title, win32con.MB_OKCANCEL)

        def send_keybd_event(keycode):
            win32api.keybd_event(
                win32con.VK_CONTROL, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0
            )
            win32api.keybd_event(keycode, 0, 0, 0)
            win32api.keybd_event(keycode, 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.keybd_event(
                win32con.VK_CONTROL,
                0,
                win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP,
                0,
            )

        hwndMain = self.working_hwndMain
        pattern.execute(hwndMain)


instance = WindowHandler(target_window="final fantasy")
# instance = WindowHandler(target_window="LOST ARK (64-bit, DX11)")
# instance = WindowHandler(target_window="Test")
pa = Pattern(1)
pa.create_pattern(["KeyPress TAB 1", "KeyPress 1 1", "Delay 2500", "KeyPress 2 1"])
instance.execute(pa)
