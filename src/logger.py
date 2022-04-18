import win32con, win32api, time
from random import uniform
from typing import Callable, Union
from functools import partial


def SendMessage(hwnd, key_action, vkey_code, lparam):
    """
    pressdown R key:
    hwndMain, win32con.WM_KEYDOWN,  0x41, 0
    """
    # print(hwnd, key_action, vkey_code, lparam)
    win32api.SendMessage(hwnd, key_action, vkey_code, lparam)


def hex_checker(keycode: Union[str, int]) -> int:
    if isinstance(keycode, str):
        return int(keycode, 16)
    elif isinstance(keycode, int):
        return keycode
    else:
        raise TypeError(
            f"keycode should be int or str type but {type(keycode)} received."
        )


def KeyDown(keycode: Union[str, int], send_function: Callable = SendMessage):
    """
    send_function should be a function takes in four arguments with names parameter (hwnd, key_action, vkey_code, lparam)
    return a function that takes in hwnd as argument
    """
    keycode = hex_checker(keycode)
    return [
        partial(
            send_function, key_action=win32con.WM_KEYDOWN, vkey_code=keycode, lparam=0
        )
    ]


def KeyUp(keycode: Union[str, int], send_function: Callable = SendMessage):
    """
    send_function should be a function takes in four arguments with names parameter (hwnd, key_action, vkey_code, lparam)
    return a function that takes in hwnd as argument
    """
    keycode = hex_checker(keycode)
    return [
        partial(
            send_function, key_action=win32con.WM_KEYUP, vkey_code=keycode, lparam=0
        )
    ]


def KeyPress(keycode: Union[str, int], send_function: Callable = SendMessage):
    """
    send_function should be a function takes in four arguments with names parameter (hwnd, key_action, vkey_code, lparam)

    return two functions that takes in hwnd as argument, one for KeyDown and another for KeyUp
    """
    keycode = hex_checker(keycode)
    return [
        partial(
            send_function, key_action=win32con.WM_KEYDOWN, vkey_code=keycode, lparam=0
        ),
        partial(
            send_function, key_action=win32con.WM_KEYUP, vkey_code=keycode, lparam=0
        ),
    ]


def sleep(hwnd, msec):
    """
    hwnd is used to make high-level function have the same input argument and omited when executes
    """
    time.sleep(msec)


def Delay(msec: int, with_random: bool = False):
    """
    randomize msec for +/- 50 msec

    sleep(10 * (0.1 + random() / 10.0) / float(0.5))
    """
    if with_random:
        msec = uniform(msec - 50, msec + 50)
    return partial(sleep, msec=msec * 0.001)
