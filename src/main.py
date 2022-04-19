import logging, os
from collections import defaultdict
from typing import DefaultDict, Dict, List, Tuple
from multiprocessing import Process
from pynput import keyboard
from KeyReader import dummy_func, on_press, on_release
from Pattern import Pattern
from Script import Script
from WindowHandler import WindowHandler
from utils import find_or_create_scripts_folder, klp_to_dict


logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s - %(asctime)s: %(message)s",
    handlers=[logging.FileHandler("keylogger.log"), logging.StreamHandler()],
)

if __name__ == "__main__":
    scripts = Script()
    scripts.retrieve_scripts(["root", "default"])
    # result = scripts.find_pattern_with_key(start_key='f10')
    # print(scripts._acting_scripts, scripts._resting_scripts)
    # print(result)
    # print("pass")

    instance = WindowHandler(target_window="final fantasy")
    # instance = WindowHandler(target_window="LOST ARK (64-bit, DX11)")
    # instance = WindowHandler(target_window="Test")

    # key_combs = {"f2": "f1", "f3":"f1"}
    # working_pattern = defaultdict(list[Tuple[Process, str]])
    # Collect events until released
    with keyboard.Listener(
        on_press=on_press(instance.execute, scripts),
        on_release=on_release(instance.execute, scripts),
    ) as listener:
        listener.join()
