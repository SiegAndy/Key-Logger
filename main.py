import logging
from uuid import uuid4
from pynput import keyboard
from src import on_press, on_release, Script, WindowHandler, Pattern, KeyCombination, Repeat


logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s - %(asctime)s: %(message)s",
    handlers=[logging.FileHandler("keylogger.log"), logging.StreamHandler()],
)


mapping = {
    "ff14": {
        "script_path": ["root", "FFIV"],
        "window_name": "final fantasy"
    },
    "lost ark": {
        "script_path": ["root", "Lost Ark"],
        "window_name": "LOST ARK (64-bit, DX11)"
    },
    "test":{
        "script_path": ["root", "default"],
        "window_name": "Test"
    }
}


def startup(map_token: str):
    target = mapping[map_token]
    scripts = Script()
    result = scripts.retrieve_scripts(target["script_path"])
    # print(result["G-4sec"].pattern)
    instance = WindowHandler(target_window=target["window_name"])
    return scripts, instance

if __name__ == "__main__":
    # logging.info(uuid4())
    logging.info("Starting Main Program...")
    scripts, instance = startup(map_token="lost ark")
    
    logging.info("Starting Keypress reading...")
    # Collect events until released
    with keyboard.Listener(
        on_press=on_press(instance.execute, scripts),
        on_release=on_release(instance.execute, scripts),
    ) as listener:
        listener.join()

    
    # instance = WindowHandler(target_window="LOST ARK (64-bit, DX11)")
    # pa = Pattern("test", repeat=Repeat(-1), key_comb=KeyCombination(start_key='f2', stop_key='f1'))
    # pa.create_pattern(["KeyPress S 1", "Delay 4000", "KeyPress G 1", "Delay 4000"])
    # instance.execute(pa)