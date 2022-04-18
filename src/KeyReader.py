import logging
from time import sleep
from pynput import keyboard
from functools import partial
from collections import defaultdict
from typing import Callable, Dict, List, Tuple
from multiprocessing import Process, current_process

SUPER_EXIT = 'f12'

def dummy_func():
    name = current_process().name

    for i in range (10):
        logging.info(f"{name} is looping")
        sleep(2)

    logging.info(f"{name} finished")


def on_press_prep(curr_key, exec_func: Callable, key_combs: Dict[str, str], working_pattern: Dict[str, List[Tuple[Process, str]]]):
    try:
        curr_char = curr_key.char
        # print(f'Alphanumeric key pressed: {curr_char}')
    except AttributeError:
        # print(f'special key pressed: {curr_key}')
        pass
def on_press(exec_func: Callable, key_combs, working_pattern):
    return partial(on_press_prep, exec_func=exec_func, key_combs=key_combs, working_pattern=working_pattern)


def on_release_prep(curr_key, exec_func: Callable, key_combs: Dict[str, str], working_pattern: Dict[str, List[Tuple[Process, str]]]):
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
        curr_key = str(curr_key).split('.')[1]
        # print(f'special key pressed: {curr_key}')

    if curr_key in key_combs.keys():
        # current key is one of start key
        stop_key = key_combs.pop(curr_key)
        # stop_key_reader = Process(target=detect_target_key, args=[stop_key], daemon=True, name=f"KeyReader_{curr}_{stop_key}")
        dummy = Process(target=exec_func, args=[], daemon=True, name=f"dummy_{curr_key}_{stop_key}")
        dummy.start()
        working_pattern[stop_key].append((dummy, curr_key))

    if curr_key in working_pattern.keys():
        # current key is one of stop key
            need_to_stop = working_pattern.pop(curr_key)
            for process, start_key in need_to_stop:
                if process.is_alive():
                    process.terminate()
                else:
                    process.close()
                logging.info(f"{process.name} terminated. start key: {start_key}, stop key:{curr_key}")
                key_combs[start_key] = curr_key

def on_release(exec_func: Callable, key_combs, working_pattern):
    return partial(on_release_prep, exec_func=exec_func, key_combs=key_combs, working_pattern=working_pattern)



if __name__ == "__main__":
    pass