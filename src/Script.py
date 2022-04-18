

import os
from typing import Dict, List
from Pattern import Pattern
from Presets import DEFAULT, create_presets
from utils import find_or_create_scripts_folder, klp_to_dict



class Script:
    """
    This class is intended to be used to manipulate 
    the current acting or resting scripts during the 
    process of listening.
    """
    def __init__(self, path: List[str] = None) -> None:
        """
        retrieve all scripts in script folder and stored in self._all_scripts

        if path is specified, acting scripts would be stored in self._scripts
            has the same effect as script=Script() + script.retrieve_scripts(path)
        """
        self._all_scripts = None
        self._scripts = None
        self.retrieve_all_scripts()
        if path is not None:
            self._scripts = self.retrieve_scripts(path=path)


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
                labels = "root" + root[len(script_path):]
            
            labels = [label for label in labels.split(os.sep) if label]
            temp = scripts
            for index, label in enumerate(labels):
                temp = temp.setdefault(label, dict())
                if index == len(labels)-1:
                    temp["files"] = files
        
        self._all_scripts = scripts

        return self._all_scripts
        

    def retrieve_scripts(self, path: List[str], scripts: Dict[str, Dict] = None) -> Dict[str, Pattern]:
        """
        path is list of string.
        e.g. path = ["root", "default"]
            it will read all scripts in path "script_folder_path/default"
        
        return a dictionary with filename as key and Pattern object as value
        """
        if scripts is None:
            scripts = self.all_scripts

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
            result[file.rstrip('.klp')] = curr_pattern
        
        return result

    def find_pattern_with_stop_key(scripts: Dict[str, Pattern], stop_key: str):
        
        fit_patterns = []
        for name, pattern in scripts.items():
            curr_start_key = pattern.key_comb.start_key
            curr_stop_key = pattern.key_comb.stop_key
            if curr_stop_key == stop_key:
                fit_patterns.append((curr_start_key, curr_stop_key, pattern))
        
        return fit_patterns


# scripts = Script()
# scripts = retrieve_all_scripts()
#     acting_scripts = retrieve_scripts(["root", "default"], scripts)

#     find_pattern_with_stop_key(acting_scripts, stop_key='f10')