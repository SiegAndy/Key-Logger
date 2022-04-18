import json
import time
from typing import Callable, List, Tuple
from logger import KeyDown, KeyUp, KeyPress, Delay

Keybd_event = ["KeyDown", "KeyUp", "KeyPress"]


class Pattern:
    """
    pattern for each key-logger event and is a list of command.
    command should be in format
        "<KeyDown|KeyUp|KeyPress> <key> [Number of Key Actions]" for keyboard event
        "Delay <msec>" for delay event
        pattern is like ["KeyDown C", "Delay 10", "KeyUp C", "Delay 10", "KeyPress C 3"]
        it means: press C down for 10 msec and relase C, delay 1000msec (1sec) and then press and release C for three times.
    """

    def __init__(
        self,
        stop_counter: int = None,
        start_counter: int = None,
        step: int = None,
        stop_time_interval: Tuple[int, int, int] = None,
    ) -> None:

        # print(start_counter, stop_counter, step, stop_time_interval)

        self.reset()
        self.mapping = self.get_vk_mapping()

        if stop_counter is not None:
            # using counters as start and stop criterion for actions/pattern
            if stop_time_interval is not None:
                raise ValueError(
                    "Counters and time interval attributes are mutually exclusive!"
                )

            self.__stop_counter = stop_counter
            self.__start_counter = start_counter
            if start_counter is not None:
                # if start_counter is not None, default step is 1
                if step is None:
                    self.__step = 1
                else:
                    self.__step = step
            else:
                # if start_counter is None, step would be ignore even if it is passed in as a valid argument
                self.__step = None

        elif stop_time_interval is not None:
            # using time interval as start and stop criterion for actions/pattern
            self.__stop_counter = None
            self.__stop_time_interval = stop_time_interval
        else:
            raise ValueError(
                "Need either counters or time interval attributes as stop criterion!"
            )

    def reset(self):
        self.pattern: List[Callable] = []

    @staticmethod
    def get_vk_mapping():
        with open("data/key_mapping.json", "r", encoding="utf-8") as input:
            return json.load(input)

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

        if self.__stop_counter is not None:

            if self.__stop_counter < 0:
                while True:
                    execute_pattern()

            elif self.__start_counter is not None:
                if self.__step is not None:
                    for i in range(
                        self.__start_counter, self.__stop_counter, self.__step
                    ):
                        execute_pattern()
                else:
                    for i in range(self.__start_counter, self.__stop_counter):
                        execute_pattern()
            else:
                for i in range(self.__stop_counter):
                    execute_pattern()

        elif self.__stop_time_interval is not None:

            hr, min, sec = self.__stop_time_interval
            timer_interval = ((hr * 60) + min * 60) + sec
            start_timer = time.time()
            end_timer = start_timer + timer_interval
            curr_timer = start_timer

            while curr_timer < end_timer:
                execute_pattern()
                curr_timer = time.time()

        else:
            raise ValueError("Unable to execute, stop criterion not set.")

        print("\nFinished execution for pattern. Exiting...")
        exit(0)
