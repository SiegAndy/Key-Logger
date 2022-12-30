import logging, os
from multiprocessing import Process
from typing import Dict, List, Tuple
from uuid import UUID
from src.utils import find_or_create_scripts_folder, klp_to_dict
from src.Pattern import Pattern
from src.Presets import DEFAULT, create_presets


class MutuallyExclusiveError(Exception):
    pass


class Script:
    """
    This class is intended to be used to manipulate
    the current acting or resting scripts during the
    process of listening.
    """

    _all_scripts: Dict[str, Dict]
    _acting_scripts: Dict[str, Pattern]
    _resting_scripts: Dict[str, Pattern]
    _working_process: Dict[UUID, Process]

    def __init__(self, path: List[str] = None) -> None:
        """
        retrieve all scripts in script folder and stored in self._all_scripts

        if path is specified, acting scripts would be stored in self._resting_scripts
            has the same effect as script=Script() + script.retrieve_scripts(path)
        """
        self.retrieve_all_scripts()
        self._acting_scripts = dict()
        self._resting_scripts = dict()
        self._working_process = dict()

        if path is not None:
            self.retrieve_scripts(path=path)

    def retrieve_all_scripts(self) -> Dict[str, Dict]:
        """
        returned scripts in format: {
            root: {
                files: [file1, file2, ...],
                filepath: {
                    files: [default_1, default_2, ...]
                    filepath: {
                        files: ...,
                        ...
                    }
                },
                another_filepath: {
                    files: [default_1, default_2, ...]
                },
                ...
            }
        }

        """
        script_path = find_or_create_scripts_folder()

        has_default = False
        if os.path.isdir(os.path.join(script_path, DEFAULT)):
            has_default = True

        scripts: Dict[str, dict] = dict()

        for root, dirs, files in os.walk(script_path):
            if len(dirs) == 0 and len(files) == 0 and not has_default:
                create_presets()
                # re-run the function again to fetch scripts in default/presets' folder
                return self.retrieve_all_scripts()

            if root == script_path:
                labels = "root"
            else:
                labels = "root" + root[len(script_path) :]

            labels = [label for label in labels.split(os.sep) if label]
            temp = scripts
            for index, label in enumerate(labels):
                temp = temp.setdefault(label, dict())
                if index == len(labels) - 1:
                    temp["files"] = files

        self._all_scripts = scripts

        return self._all_scripts

    def retrieve_scripts(
        self, path: List[str], scripts: Dict[str, Dict] = None
    ) -> Dict[str, Pattern]:
        """
        path is list of string.
        e.g. path = ["root", "default"]
            it will read all scripts in path "script_folder_path/default"

        return a dictionary with filename as key and Pattern object as value
        """
        if scripts is None:
            scripts = self._all_scripts

        result = dict()
        script_folder_path = find_or_create_scripts_folder()
        files = scripts
        for subpath in path:
            files = files[subpath]
            if subpath == "root":
                continue
            script_folder_path = os.path.join(script_folder_path, subpath)

        for file in files["files"]:
            curr_path = os.path.join(script_folder_path, file)
            curr_pattern_dict = klp_to_dict(filename=curr_path)
            # print(curr_pattern_dict)
            curr_pattern = Pattern.fromDict(curr_pattern_dict)
            result[file.rstrip(".klp")] = curr_pattern

        self._resting_scripts = result
        return self._resting_scripts

    def find_pattern_with_key(self, **key) -> List[Tuple[str, str, Pattern]]:
        """
        key should be in format start_key=key_name or stop_key=key_name
        """
        if len(key) != 1:
            raise TypeError("Need exact one named argument.\ne.g. start_key=key_name")
        compared_key = key.get("start_key")
        if compared_key is None:
            compared_key = key.get("stop_key")
            if compared_key is None:
                raise TypeError(
                    "Need exact one named argument.\ne.g. start_key=key_name"
                )
            key_type = "stop_key"
            scripts = self._acting_scripts
            appending_scripts = self._resting_scripts
            # if query for stop_key, we want to have acting scripts which might need to be stopped
        else:
            if key.get("stop_key") is not None:
                raise MutuallyExclusiveError(
                    "You can only query either start_key or stop_key!"
                )
            key_type = "start_key"
            scripts = self._resting_scripts
            appending_scripts = self._acting_scripts
            # if query for start_key, we want to have resting scripts which might need to be started

        # logging.warn("----------before----------")
        # logging.warn(key_type)
        # logging.warn(self._acting_scripts)
        # logging.warn(self._resting_scripts)

        fit_patterns = []
        need_to_remove = []
        for name, pattern in scripts.items():
            curr_start_key = pattern.key_comb.start_key
            curr_stop_key = pattern.key_comb.stop_key
            if key_type == "start_key" and curr_start_key == compared_key:
                # logging.warn((curr_start_key, compared_key))
                need_to_remove.append(name)
                fit_patterns.append((curr_start_key, curr_stop_key, pattern))
            elif key_type == "stop_key" and curr_stop_key == compared_key:
                need_to_remove.append(name)
                fit_patterns.append((curr_start_key, curr_stop_key, pattern))

        for elem in need_to_remove:
            value = scripts.pop(elem)
            appending_scripts[elem] = value

        # logging.warn(need_to_remove)
        # logging.warn(key_type)
        # logging.warn(self._acting_scripts)
        # logging.warn(self._resting_scripts)
        # logging.warn("----------after----------")
        return fit_patterns

    def add_process(self, process_id: UUID, new_process: Process) -> None:
        """
        add process according to process_id

        process_id should be Pattern.uuid
        """
        self._working_process[process_id] = new_process
        # logging.info(self._working_process)

    def remove_process(self, process_id: UUID) -> Process:
        """
        remove process according to process_id

        process_id should be Pattern.uuid
        """
        try:
            return self._working_process.pop(process_id)
        except KeyError as e:
            # Error could happen when process is already ended and removed but listener thread does not aware of it
            logging.warn(f"Missing key: {process_id}")
            return None
