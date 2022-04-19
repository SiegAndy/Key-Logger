import os
from typing import List
from src.Pattern import Pattern
from src.utils import (
    create_directory,
    dict_to_klp,
    find_or_create_scripts_folder,
)


DEFAULT = "default"

preset_commands = [
    [
        "KeyPress TAB 1",
        "KeyPress 1 1",
        "Delay 2500",
        "KeyPress 2 1",
        "Delay 2500",
        "KeyPress 3 1",
    ]
]


def create_presets(presets: List[List[str]] = preset_commands):

    script_path = find_or_create_scripts_folder()
    create_directory(os.path.join(script_path, DEFAULT))

    for index, preset in enumerate(presets):
        pattern = Pattern(f"default_pattern_{index}")
        pattern.create_pattern(preset)
        filename = os.path.join(DEFAULT, pattern.name)
        dict_to_klp(filename, pattern.toDict())
