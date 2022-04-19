import os, re
from typing import Any, Dict, List, Union
from .filesystem import create_directory, find_dir

"""
klp is abbreviation of key-logger-pattern. 
A file contains a pattern that would be send to WindowHandler to execute at designated window.
Default storage folder would be at ~/src/scripts

It accepts dictionary or object.__dict__ to be converted as specific format of string and stored in *.klp
"""


class FormatError(Exception):
    pass


def find_or_create_scripts_folder():
    src_path = find_dir("src", up=1)
    if src_path is not None:
        return create_directory(os.path.join(src_path, "scripts"))
    else:
        return create_directory("scripts")


def dict_to_klp(filename: str, object: Dict[Any, dict], indent: int = 0):
    """
    filename should be same as the name attribute in Pattern object
    object should be in format {
        <category>: {
            attribute_1: value_1,
            attribute_2: value_2,
            ...
        }
        ...
    }

    return klp string
    """

    indent = " " * indent
    contents = ""
    for category, elements in object.items():
        contents += f"[{category}]\n"
        if "script" in category.lower():
            for line in elements:
                contents += f"{line}\n"
        else:
            for attribute, value in elements.items():
                contents += f"{indent}{attribute}={value}\n"

    script_path = find_or_create_scripts_folder()

    with open(
        os.path.join(script_path, f"{filename}.klp"), "w", encoding="utf-8"
    ) as klp:
        klp.write(contents)

    return contents


def klp_to_dict(filename: str):
    """
    filename should be full path (relative or absolute)

    object should be in format {
        <category>: {
            attribute_1: value_1,
            attribute_2: value_2,
            ...
        }
        ...
    }
    """
    category_pattern = r"\[(.*)\]"
    attribute_pattern = r"(.*)=(.*)"

    re_category = re.compile(category_pattern)
    re_attribute = re.compile(attribute_pattern)

    with open(filename, "r", encoding="utf-8") as input:

        contents = input.readlines()
        result_dict: Dict[str, Union[Dict, List]] = dict()
        current_category = None
        is_script = False

        for line in contents:
            if line is None:
                continue

            line = line.strip("\n")
            if (
                current_category is not None
                and "script" not in current_category.lower()
            ):
                # remove indents which are whitespace for every non-script section
                line = [elem for elem in line.split(" ") if elem][0]

            attribute_value = re_attribute.match(line)
            category = re_category.match(line)
            # print(f"current line: {line}, {is_script}")

            if attribute_value is not None:
                # means it is a attribute string
                if current_category is None:
                    raise FormatError(
                        "You must first have a category and then assign attribute!"
                    )

                attribute, value = attribute_value.group(1), attribute_value.group(2)
                result_dict[current_category][attribute] = value
            elif category is not None:
                # means it is a category string
                # reset is_script every time encounter a category line
                is_script = False
                category = category.group(1)
                result_dict[category] = dict()
                # print("script" in category.lower())
                if "script" in category.lower():
                    result_dict[category] = list()
                    is_script = True
                current_category = category
            elif is_script:
                # means it is a Script line should be append to list
                result_dict[current_category].append(line)
            else:
                print(is_script)
                raise ValueError(f"Unable to identify line: '{line}'")

    return result_dict
