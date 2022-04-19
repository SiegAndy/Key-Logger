import logging
from uuid import uuid4
from pynput import keyboard
from KeyReader import on_press, on_release
from Script import Script
from WindowHandler import WindowHandler


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
    scripts.retrieve_scripts(target["script_path"])
    instance = WindowHandler(target_window=target["window_name"])
    return scripts, instance

if __name__ == "__main__":
    logging.info(uuid4())
    logging.info("Starting Main Program...")
    scripts, instance = startup(map_token="ff14")
    
    logging.info("Starting Keypress reading...")
    # Collect events until released
    with keyboard.Listener(
        on_press=on_press(instance.execute, scripts),
        on_release=on_release(instance.execute, scripts),
    ) as listener:
        listener.join()
