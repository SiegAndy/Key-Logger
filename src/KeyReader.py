import logging
from time import sleep
from pynput import keyboard
from functools import partial
from collections import defaultdict
from typing import Callable, Dict, List, Tuple
from multiprocessing import Process, current_process

from src.Script import Script

SUPER_EXIT = "f12"


def dummy_func():
    name = current_process().name

    for i in range(10):
        logging.info(f"{name} is looping")
        sleep(2)

    logging.info(f"{name} finished")


def on_press_prep(curr_key, exec_func: Callable, scripts: Script):
    try:
        curr_char = curr_key.char
        # print(f'Alphanumeric key pressed: {curr_char}')
    except AttributeError:
        # print(f'special key pressed: {curr_key}')
        pass


def on_press(exec_func: Callable, scripts: Script):
    return partial(on_press_prep, exec_func=exec_func, scripts=scripts)


def on_release_prep(curr_key, exec_func: Callable, scripts: Script):
    """
    scripts should be a initialized Script object which have two sets: acting and resting scripts.

    Query start_key or stop_key from scripts would transfer script from one set to another.

    Each script would be a Pattern object, which should be passed in as argument to exec_func

    """
    # print(f'Key released: {int(curr_key)}')
    if curr_key == keyboard.Key[SUPER_EXIT]:
        # exit on the super exit key
        logging.info("Terminating keyboard listener. Exiting program...")
        return False

    try:
        curr_key = curr_key.char
        # print(f'Alphanumeric key pressed: {curr_key}')
    except AttributeError:
        # special key are presented in format Key.{special}
        curr_key = str(curr_key).split(".")[1]
        # print(f'special key pressed: {curr_key}')

    # currently number on numpad cannot be properly detected and None is received.
    if curr_key is None or curr_key == "":
        return

    # find patterns that current key is served as start key
    start_set = scripts.find_pattern_with_key(start_key=curr_key)
    # find patterns that current key is served as stop key
    stop_set = scripts.find_pattern_with_key(stop_key=curr_key)

    if len(start_set) == 0 and len(stop_set) == 0:
        logging.info(
            f"Detected Keypress: '{curr_key}'. No valid Process started/terminated..."
        )

    # logging.info("start")
    # logging.info(start_set)
    # logging.info("stop")
    # logging.info(stop_set)

    for curr_start_key, curr_stop_key, start_pattern in start_set:
        process_name = start_pattern.name
        process_id = start_pattern.uuid
        curr_process = Process(
            target=exec_func,
            args=[start_pattern],
            daemon=True,
            name=f"{process_name}_{curr_start_key}_{curr_stop_key}",
        )
        logging.info(
            f"{curr_process.name} started. start key: {curr_start_key}, stop key:{curr_stop_key}"
        )
        curr_process.start()
        scripts.add_process(process_id=process_id, new_process=curr_process)

    for curr_start_key, curr_stop_key, stop_pattern in stop_set:
        process_id = stop_pattern.uuid
        need_to_stop_process = scripts.remove_process(process_id=process_id)
        if need_to_stop_process is None:
            logging.info(
                f"{process_id} cannot be terminated. Unable to find process according to id."
            )
            return 

        if need_to_stop_process.is_alive():
            need_to_stop_process.terminate()
        else:
            need_to_stop_process.close()
        logging.info(
            f"{need_to_stop_process.name} terminated. start key: {curr_start_key}, stop key:{curr_stop_key}"
        )


def on_release(exec_func: Callable, scripts: Script):
    return partial(on_release_prep, exec_func=exec_func, scripts=scripts)


if __name__ == "__main__":
    pass
