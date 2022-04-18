import os
import re
import shutil


def find_file(filename: str, default_dir: str = None, up=0) -> str:
    result = os.path.isfile(filename)

    if not result:
        if default_dir != None:
            try:
                fn = os.path.join(default_dir, filename)
                result = find_file(filename=fn, up=up)
            except FileNotFoundError:
                result = find_file(filename=filename, up=up)
            return result
        else:
            if up != 0:
                return find_file(filename=filename, default_dir=default_dir, up=(up - 1))
            for root, dirs, files in os.walk("."):
                for file in files:
                    if file == filename:
                        return os.path.join(root, file)

        raise FileNotFoundError(f"Unable to find {filename} in current directory.")

    return filename


def find_dir(dir_name: str, up: int = 0, walking_path: str = ".") -> str:
    result = os.path.isdir(dir_name)
    if not result:
        if up > 0:
            if walking_path == '.':
                walking_path = os.path.join("..","")
            else:
                walking_path = os.path.join("..", walking_path)
            return find_dir(dir_name=dir_name, up=(up - 1), walking_path=walking_path)
        # print("pass")
        # print(f"{dir_name} {up} {walking_path}")
        for root, dirs, files in os.walk(walking_path):
            # print(root, dirs, files)
            for dir in dirs:
                if dir == dir_name:
                    return os.path.join(root, dir)
        raise FileNotFoundError(f"Unable to find {dir_name} in current directory.")
    return dir_name

print( )
def reformat_directory(target_dir: str):
    """
    reformat directory name with current system's seperator
    """
    without_slash = [inner for outter in target_dir.split('\\') for inner in outter.split('/') if inner]
    return os.path.join(*without_slash)


def check_directory(target_dir: str, compare_dir: str = os.getcwd()) -> bool:
    """
    compare target_dir and see if that match last part of compare_dir
    """
    target_dir = reformat_directory(target_dir)
    compare_dir = reformat_directory(compare_dir)
    
    if len(target_dir) > len(compare_dir):
        # no way that target_dir has longer length while still be part of compare_dir
        return False
    
    if compare_dir[-len(target_dir):] == target_dir:
        # if target_dir match the last len(target_dir) character return True
        return True

    return False


def remove_directory(datapath: str):
    try:
        shutil.rmtree(datapath)
    except:
        pass


def create_directory(datapath: str, default_dir: str = None, up=0):
    try:
        datapath = find_dir(dir_name=datapath, up=up)
    except FileNotFoundError:
        try:
            os.makedirs(datapath)
        except Exception as e:
            if default_dir != None:
                return default_dir
            else:
                raise OSError(f"Unable to create directory: {datapath}")
    return datapath
