import os
import functools
from abc import ABC, abstractmethod
from typing import Callable


# CORE INTERPRETER STUFF
COMMANDS = {}


def register_cmd(cmd_name):
    def wrapper(func):
        if cmd_name not in COMMANDS:
            COMMANDS[cmd_name] = func
        return func
    return wrapper


class Command(ABC):
    def check(self, args):
        return True
    
    def run(self, args, interpreter=None):
        pass

    def receive_output(self, output_data: str):
        pass

    def parse_output(self):
        pass
    
    def clear_output(self):
        self.output = ""


class PromptInterpreter:
    def __init__(self):
        self.current_cmd = None
        self.cmd_processors = {}
        self.cwd = []

    def process_cmd(self, prompt: str):
        words = prompt.split(" ")
        cmd_name, args = words[0].strip(), list(map(str.strip, words[1:]))
    
        cmd_class = COMMANDS.get(cmd_name, None)
        if not cmd_class:
            raise Exception(f"Error: Command {cmd_name} not found!")
        
        cmd_obj = cmd_class()
        self.current_cmd = cmd_obj
        
        if not cmd_obj.check(args):
            raise Exception(f"Error while parsing command {type(cmd_obj).__name__}")
        
        cmd_obj.run(args, interpreter=self)
    
    def receive_output(self, output_data: str):
        if self.current_cmd:
            self.current_cmd.receive_output(output_data)

    def register_cmd_output_processor(self, cmd: Command, func: Callable, *args, **kwargs):
        if cmd not in self.cmd_processors:
            self.cmd_processors[cmd] = []
        self.cmd_processors[cmd].append((func, args, kwargs))

    def on_cmd_end(self):
        if not self.current_cmd:
            raise Exception("Error: No command running!")
        
        cmd = self.current_cmd
        parsed_data = cmd.parse_output()
        cmd.clear_output()
        self.current_cmd = None
        processors = self.cmd_processors.get(type(cmd), [])
        for p in processors:
            func, args, kwargs = p
            func(parsed_data, interpreter, *args, **kwargs) 


# TREE NAVIGATION HELPERS
def find(tree_node: dict, predicate: Callable, cwd: list = None):
    results = []

    if cwd is None:
        cwd = []

    for fs_obj in tree_node:
        if predicate(tree_node[fs_obj], cwd + [fs_obj]):
            results.append(cwd + [fs_obj])

        if type(tree_node[fs_obj]) == dict:
            results.extend(find(tree_node[fs_obj], predicate, cwd + [fs_obj]))
    
    return results


def get_file(tree_node: dict, path: list):
    curr_node = tree_node

    for d in path:
        curr_node = curr_node[d]
    
    return curr_node


def get_files_in_folder(tree_node: dict, path: list):
    return find(tree_node, lambda f, cwd: path == cwd[:len(path)] and type(f) is not dict)


def get_folder_size(tree_node: dict, path: list):
    return sum(list(map(lambda p: int(get_file(tree_node, p)), get_files_in_folder(tree_node, path))))



# COMMANDS
@register_cmd('cd')
class ChangeDirectoryCommand(Command):
    output = ""

    def check(self, args):
        return len(args) >= 1
        
    def run(self, args, interpreter=None):
        if interpreter is None:
            raise Exception("Error: No interpreter in parameter!")

        fs_obj = args[0]
        if fs_obj == "..":
            interpreter.cwd = interpreter.cwd[:-1]
        else:
            interpreter.cwd.append(fs_obj)


@register_cmd('ls')
class ListDirectoryCommand(Command):
    output = ""

    def receive_output(self, output_data: str):
        self.output += output_data

    def parse_output(self):
        fs_obj_list = self.output.strip().split('\n')

        parsed_data = {}

        for fs_obj in fs_obj_list:
            parsed_fs_obj = fs_obj.split(" ")
            size, fs_obj_name = parsed_fs_obj[0], "".join(parsed_fs_obj[1])
            parsed_data[fs_obj_name] =  size
        
        return parsed_data
    



if __name__ == "__main__":
    TREE = {"/": {}}

    with open(os.path.dirname(__file__) + "/input.txt") as fp:
        data = fp.readlines()

    interpreter = PromptInterpreter()

    def update_tree_with_ls_cmd_output(output_data, interpreter, tree):
        filelist = output_data
        curr_tree_node = tree

        for d in interpreter.cwd:
            if d in curr_tree_node and type(curr_tree_node[d]) is not dict:
                raise Exception(f"Trying to walk into {d} which is not a directory!")
            
            if d not in curr_tree_node:
                curr_tree_node[d] = {}
            
            curr_tree_node = curr_tree_node[d]

        for filename in filelist:
            if filelist[filename] == "dir":
                curr_tree_node[filename] = {}
            else:
                curr_tree_node[filename] = filelist[filename]

    interpreter.register_cmd_output_processor(ListDirectoryCommand, update_tree_with_ls_cmd_output, TREE)

    # PART 0
    DRIVE_SIZE = 70000000
    UPDATE_SIZE = 30000000

    # Reading replay log and feeding commands to interpreter
    for i, l in enumerate(data):
        output = ""

        if l.startswith("$"):
            if interpreter.current_cmd:
                interpreter.on_cmd_end()
                
            interpreter.process_cmd(l[1:].strip())
        else:
            interpreter.receive_output(l)

    interpreter.on_cmd_end()

    folder_list = find(TREE, lambda fs_obj, cwd: type(fs_obj) is dict)
    #print(f"{folder_list=}")

    # PART 1
    directories_with_max_size = list(filter(lambda p: get_folder_size(TREE, p) < 100000, folder_list))
    total_small_dirs_size = sum(map(lambda d: get_folder_size(TREE, d), directories_with_max_size))
    print(f"{total_small_dirs_size=}")

    # PART 2
    total_size = get_folder_size(TREE, ['/'])
    print(f"{total_size=}")

    space_to_restore = UPDATE_SIZE - (DRIVE_SIZE - total_size)
    print(f"{space_to_restore=}")

    directories_with_max_size = list(filter(lambda p: get_folder_size(TREE, p) >= space_to_restore, folder_list))
    print(f"{directories_with_max_size=}")

    smallest_big_folder_path = list(sorted(directories_with_max_size, key=lambda p: get_folder_size(TREE, p)))[0]
    smallest_big_folder_size = get_folder_size(TREE, smallest_big_folder_path)
    print(f"{smallest_big_folder_size=} ({smallest_big_folder_path})")
