import msvcrt
from typing import Union


# msvcrt function key mapping
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


Reverse_Mapping = {}
for key, value in FUNCTIONKEY.items():
    Reverse_Mapping[value] = key


def detect_key_kbhit() -> Union[None, str]:
    """
    Convert every valid keypress to key name and return that key name
    Default return None otherwise
    """
    if msvcrt.kbhit():
        ret = ord(msvcrt.getch())
        # print(ret)
        if ret == 0 or ret == 224:
            second = ord(msvcrt.getch())
            return Reverse_Mapping[(ret, second)]
        else:
            return chr(ret)


def detect_target_key_kbhit(ascii_code):
    """
    Check whether received keypress code is the target key's ascii code
    """
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


def detect_target_key(key):
    """
    Loop until target_key is found
    # When looping, it will keep yield False
    After loop terminate, it will return True
    """
    try:
        ascii_code = FUNCTIONKEY[key]
    except KeyError as e:
        ascii_code = [ord(key)]
    while not detect_target_key_kbhit(ascii_code):
        pass
    return True


def detect_key():
    """
    Looping endless for detecting activate key for each pattern
    """
    while True:
        curr = detect_key_kbhit()
        if curr is not None:
            print(curr)
        
    
# detect_key()