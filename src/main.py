
from collections import defaultdict
import logging
from multiprocessing import Process, current_process
from time import sleep
from typing import List, Tuple
from KeyReader import detect_key_kbhit, detect_target_key


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    handlers=[logging.FileHandler("example1.log"),
                              logging.StreamHandler()])


def dummy_func():
    name = current_process().name

    for i in range (10):
        logging.info(f"{name} is looping")
        sleep(2)

    logging.info(f"{name} finished")


if __name__ == "__main__":
    key_comb = {"F2": "F1", "F3":"F1"}
    working_pattern = defaultdict(list[Tuple[Process, str]])

    while True:
        curr = detect_key_kbhit()
        if curr in key_comb.keys():
            stop_key = key_comb.pop(curr)
            # stop_key_reader = Process(target=detect_target_key, args=[stop_key], daemon=True, name=f"KeyReader_{curr}_{stop_key}")
            dummy = Process(target=dummy_func, args=[], daemon=True, name=f"dummy_{curr}_{stop_key}")
            dummy.start()
            working_pattern[stop_key].append((dummy, curr))
        if curr in working_pattern.keys():
            need_to_stop = working_pattern.pop(curr)
            for process, start_key in need_to_stop:
                if process.is_alive():
                    process.terminate()
                logging.info(f"{process.name} terminated. start key: {start_key}, stop key:{curr}")
                key_comb[start_key] = curr
