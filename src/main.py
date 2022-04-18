

import logging, os
from collections import defaultdict
from typing import DefaultDict, Dict, List, Tuple
from multiprocessing import Process
from pynput import keyboard
from KeyReader import dummy_func, on_press, on_release
from Pattern import Pattern
from WindowHandler import WindowHandler
from utils import find_or_create_scripts_folder, klp_to_dict



logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s - %(asctime)s: %(message)s',
                    handlers=[logging.FileHandler("keylogger.log"),
                              logging.StreamHandler()])

if __name__ == "__main__":
    pass

    # instance = WindowHandler(target_window="final fantasy")
    # instance = WindowHandler(target_window="LOST ARK (64-bit, DX11)")
    # instance = WindowHandler(target_window="Test")

    # key_combs = {"f2": "f1", "f3":"f1"}
    # working_pattern = defaultdict(list[Tuple[Process, str]])
    # # Collect events until released
    # with keyboard.Listener(
    #         on_press=on_press(dummy_func, key_combs, working_pattern),
    #         on_release=on_release(dummy_func, key_combs, working_pattern)) as listener:
    #     listener.join()