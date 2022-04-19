import time, logging
from uuid import UUID, uuid4
from multipledispatch import dispatch
from typing import Callable, Dict, List
from Logger import KeyDown, KeyUp, KeyPress, Delay
from utils import mapping


Keybd_event = ["KeyDown", "KeyUp", "KeyPress"]


def dict_to_object(cls: object, input_dict: Dict[str, Dict]):
    # print(input_dict)
    for attribute, value in input_dict.items():
        if 'uuid' in attribute.lower():
            continue
        key = '_' + attribute
        try:
            value = int(value)
        except:
            pass
        setattr(cls, key, value)
    # print(self.__dict__)
    return cls


class stringifyable:
    
    category = "Stringifyable"

    @dispatch()
    def __init__(self) -> None:
        pass

    def stringify(self):

        # print(self.__dict__)
        result = f"[{self.category}]\n"
        for name, value in self.__dict__.items():
            result += f"{name.lstrip('_')}={value}\n"
        return result
    
    def unstringify(self, load_string: str):

        attributes = [elem for elem in load_string.split('\n') if elem]
        if attributes[0] == f"[{self.category}]":
            attributes = attributes[1:]

        for attribute in attributes:
            if 'uuid' in attribute.lower():
                continue
            key, value = attribute.split('=')
            key = '_' + key
            try:
                value = int(value)
            except:
                pass
            setattr(self, key, value)
        # print(self.__dict__)
        return self
    
    def toDict(self):
        result = dict()
        result[self.category] = dict()
        for name, value in self.__dict__.items():
            result[self.category][name.lstrip('_')] = value
        # print(result)
        return result

    @classmethod
    def fromDict(cls, input_dict: Dict[str, Dict]):
        cls = cls()
        return dict_to_object(cls=cls, input_dict=input_dict)


class KeyCombination(stringifyable):
    """
    key combination for start key and stop key (which start and stop the script)
    """
    category = "Keys"

    def __getitem__(self, item):
        return getattr(self, item)


    def __init__(
        self,
        start_key: str = "f10",
        stop_key: str = "f11"
    ) -> None:
        self._start_key = start_key
        self._stop_key = stop_key


    @property
    def start_key(self):
        return self._start_key


    @start_key.setter
    def start_key(self, new_start_key: str):
        self._start_key = new_start_key
        return self._start_key
    

    @property
    def stop_key(self):
        return self._stop_key


    @stop_key.setter
    def stop_key(self, new_stop_key: str):
        self._stop_key = new_stop_key
        return self._stop_key


class Repeat(stringifyable):
    """
    Repeat type for Pattern class
        Type I (0): start_counter, stop_counter, step => similar to Range
        Type II (1): stop_time_interval [hr, min, sec] => stop at <hr> hour <min> minute <sec> seconds

    """
    category = "Repeat"

    @dispatch()
    def __init__(self) -> None:
        pass

    @dispatch(int, start_key=str, stop_key=str)
    def __init__(
        self,
        stop_counter: int,
    ) -> None:
        self._type = 0
        self._stop_counter = stop_counter
        self._start_counter = None
        self._step = None
        

    @dispatch(int, start_counter=int, step=int, start_key=str, stop_key=str)
    def __init__(
        self,
        stop_counter: int,
        start_counter: int = 0,
        step: int = 1,
    ) -> None:
        self._type = 0
        self._stop_counter = stop_counter
        self._start_counter = start_counter
        self._step = step


    @dispatch(float, min=int, hr=int, start_key=str, stop_key=str)
    def __init__(
        self,
        sec: float,
        min: int = 0,
        hr: int = 0,
    ) -> None:
        self._type = 1
        self._sec = sec
        self._min = min
        self._hr = hr


    def execute(self, func: Callable):
        if self._type == 0:
            if self._stop_counter < 0:
                while True:
                    # only stop when stop key is pressed
                    func()

            elif self._start_counter is not None:
                # if we have a start counter
                if self._step is not None:
                    # if the step is set, create a for loop from range object with start, stop, step set.
                    for i in range(
                        self._start_counter, self._stop_counter, self._step
                    ):
                        func()
                else:
                    # if the step is not set, create a for loop from range object with start and stop set.
                    for i in range(self._start_counter, self._stop_counter):
                        func()
            else:
                # if the start counter is not set, create a for loop from range object with stop set.
                for i in range(self._stop_counter):
                    func()

        elif self._type == 1:

            timer_interval = ((self._hr * 60) + self._min * 60) + self._sec
            start_timer = time.time()
            end_timer = start_timer + timer_interval
            curr_timer = start_timer

            while curr_timer < end_timer:
                func()
                curr_timer = time.time()

        else:
            raise ValueError("Unable to execute, stop criterion not set.")

        return True



DEFAULTREPEAT = Repeat(1)
DEFAULTCOMB = KeyCombination()
SCRIPT = "Script"

class Pattern(stringifyable):
    """
    pattern for each key-logger event and is a list of command.
    command should be in format
        "<KeyDown|KeyUp|KeyPress> <key> [Number of Key Actions]" for keyboard event
        "Delay <msec>" for delay event
        pattern is like ["KeyDown C", "Delay 10", "KeyUp C", "Delay 1000", "KeyPress C 3"]
        it means: press C down for 10 msec and relase C, delay 1000msec (1sec) and then press and release C for three times.
    """
    
    @dispatch()
    def __init__(self) -> None:
        self.reset()


    @dispatch(str, repeat=Repeat, key_comb=KeyCombination)
    def __init__(
        self,
        name: str,
        repeat: Repeat = None,
        key_comb: KeyCombination = None,
    ) -> None:

        # print(start_counter, stop_counter, step, stop_time_interval)

        self._name = name
        self._uuid = uuid4()

        self._repeat = repeat
        if repeat is None:
            self._repeat = DEFAULTREPEAT

        self._key_comb = key_comb
        if key_comb is None:
            self._key_comb = DEFAULTCOMB

    @property
    def repeat(self) -> Repeat:
        return self._repeat
    
    @property
    def key_comb(self) -> KeyCombination:
        return self._key_comb

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, new_name: str) -> str:
        self._name = new_name
        return self._name
    
    @property
    def uuid(self) -> UUID:
        return self._uuid
    
    @uuid.setter
    def uuid(self, new_uuid: UUID) -> UUID:
        self._uuid = new_uuid
        return self._uuid
        
    def reset(self):
        self.pattern: List[Callable] = []
        self.mapping = mapping


    def create_pattern(self, commands: List[str]):
        def create_keyboard_command(action, key, num):
            try:
                curr_vk = self.mapping[key]
                curr_vk = curr_vk["virtual_key"]
                num = int(num)
            except KeyError:
                raise KeyError(f"Unable to find mapping for key '{key}'.")
            except Exception as e:
                raise KeyError(e.args[0])

            result_command = []
            if action in Keybd_event:
                target_func = globals()[action]
                for i in range(num):
                    result_command += target_func(keycode=curr_vk)
                return result_command
            else:
                raise ValueError(f"Unknown action for keyboard event: {action}")

        def create_delay_command(msec: float):
            if not isinstance(msec, float):
                try:
                    msec = float(msec[0])
                except Exception as e:
                    raise ValueError(
                        f"{e.args[0]}.\nUnable to convert command to float, command: {msec}."
                    )
            return [globals()["Delay"](msec)]

        def extract_command(command: str):
            def helper(command):
                if len_command == 1:
                    key = command
                    num = 1
                elif len_command == 2:
                    key, num = command
                else:
                    raise ValueError(
                        f"Required arguments number: 2 or 3, but {len_command} received"
                    )
                return key, num

            # retrieve elements in command by splitting on whitespace
            action, *command = [elem for elem in command.split(" ") if elem]
            len_command = len(command)

            if action in Keybd_event:
                key, num = helper(command=command)
                return create_keyboard_command(action=action, key=key, num=num)
            elif action == "Delay":
                if len_command != 1:
                    raise ValueError(
                        f"Required arguments number: 2, but {len_command} received"
                    )
                return create_delay_command(msec=command)

        self.reset()

        self.commands = commands

        for command in commands:
            if not isinstance(command, str):
                raise ValueError(
                    f"command should be a string but {type(command)} received"
                )
            self.pattern += extract_command(command=command)

        return self.pattern


    def execute(self, hwnd):
        def execute_pattern():
            print(self.pattern)
            for command in self.pattern:
                command(hwnd)

        self._repeat.execute(execute_pattern())

        logging.info("\nFinished execution for pattern.")
    

    def stringify(self):
        general = self._key_comb.stringify()
        general += f"uuid={self._uuid}\n"
        general += f"name={self._name}\n"
        repeat = self._repeat.stringify()
        script = "[Script]\n"
        for command in self.commands:
            script += f"{command}\n"
        
        return general + repeat + script

    
    def unstringify(self, load_string: str):
        # split on Repeat object's category flag
        general, repeat_script = load_string.split(f"[{DEFAULTREPEAT.category}]")

        # retrieve uuid from string
        self._uuid = [elem for elem in general.split('\n') if elem][-1].split('=')[1]

        # retrieve key combination from string
        self._key_comb = KeyCombination().unstringify(general)

        # split on script's category flag
        repeat, script = repeat_script.split("[Script]")

        # retrieve repeat style from string
        self._repeat = Repeat().unstringify(repeat)

        # retrieve commands from string
        commands = [elem for elem in script.split("\n") if elem]

        # create pattern according to commands
        self.create_pattern(commands)

        return self

    def toDict(self):
        general = self._key_comb.toDict()
        # print(general)
        general_category = self._key_comb.category
        general[general_category]["name"] = self._name
        general[general_category]["uuid"] = self._uuid

        repeat = self._repeat.toDict()

        pattern = {**general, **repeat}

        if self.commands is not None:
            pattern[SCRIPT] = self.commands
        
        return pattern

    @classmethod
    def fromDict(cls, input_dict: Dict[str, Dict]):
        cls = cls()
        # print(input_dict)
        general = input_dict[DEFAULTCOMB.category]
        repeat = input_dict[DEFAULTREPEAT.category]
        scripts = input_dict[SCRIPT]

        name = general.pop("name")
        uuid = general.pop("uuid")
        setattr(cls, "_name", name)
        setattr(cls, "_uuid", uuid)

        key_comb = KeyCombination.fromDict(input_dict=general)
        setattr(cls, "_key_comb", key_comb)

        repeat = KeyCombination.fromDict(input_dict=repeat)
        setattr(cls, "_repeat", repeat)
        
        # print(scripts)
        if scripts is not None:
            cls.create_pattern(scripts)

        return cls