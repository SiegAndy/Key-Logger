import msvcrt
import threading


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


FUNCTIONKEY = {
    "F1": (0, 59),
    "F2": (0, 60),
    "F3": (0, 61),
    "F4": (0, 62),
    "F5": (0, 63),
    "F6": (0, 64),
    "F7": (0, 65),
    "F8": (0, 66),
    "F9": (0, 67),
    "F10": (0, 68),
    "F11": (0, 69),
    "F12": (224, 134),
    "INS": (224, 82),
    "HOME": (224, 71),
    "PageUp": (224, 73),
    "DEL": (224, 83),
    "END": (224, 79),
    "PageDown": (224, 81),
    "Arrow Up": (224, 72),
    "Arrow Down": (224, 80),
    "Arrow Left": (224, 75),
    "Arrow Right": (224, 77),
}


def detect_key_kbhit(ascii_code):
    if msvcrt.kbhit():
        ret = ord(msvcrt.getch())
        # print(ret)
        if (ret == 0 or ret == 224) and ascii_code[0] == ret and len(ascii_code) == 2:
            second = ord(msvcrt.getch())
            # print(second)
            if second == ascii_code[1]:
                return True
        elif ascii_code[0] == ret and len(ascii_code) == 1:
            return True
    return False


def detect_key(key):
    try:
        ascii_code = FUNCTIONKEY[key]
    except KeyError as e:
        ascii_code = [ord(key)]
    while not detect_key_kbhit(ascii_code):
        pass
    return True
