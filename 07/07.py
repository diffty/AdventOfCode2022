import os

COMMANDS = {}


def register_cmd(cmd_name):
    def wrapper(func):
        if cmd_name not in COMMANDS:
            COMMANDS[cmd_name] = func
        return func
    return wrapper


@register_cmd('cd')
class ChangeDirectoryCommand:
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

    def receive_output(self, output_data: str):
        pass

    def parse_output(self):
        pass
    
    def clear_output(self):
        self.output = ""


@register_cmd('ls')
class ListDirectoryCommand:
    output = ""

    def check(self, args):
        return True
        
    def run(self, args, interpreter=None):
        pass

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
    
    def clear_output(self):
        self.output = ""


class PromptInterpreter:
    def __init__(self):
        self.current_cmd = None
        self.cwd = []

    def process_cmd(self, prompt: str):
        words = prompt.split(" ")
        print(f"{words=}")
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

    def on_cmd_end(self):
        if self.current_cmd:
            cmd = self.current_cmd
            parsed_data = cmd.parse_output()
            cmd.clear_output()
            self.current_cmd = None
            return cmd, parsed_data


def update_tree_using_cmd_output(tree, interpreter, output_data):
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


def get_size_directory(tree, predicat=None):
    size = 0

    for fs_obj in tree:
        if type(tree[fs_obj]) == dict:
            size += get_size_directory(tree[fs_obj])
        else:
            size += int(tree[fs_obj])
    

    return size


def find_directory_with_max_size(tree, size_max, cwd=None):
    if cwd == None:
        cwd = []

    found_dirs = []

    for fs_obj in tree:
        cwd.append(fs_obj)
        if type(tree[fs_obj]) == dict:
            dir_size = get_size_directory(tree[fs_obj])

            if dir_size <= size_max:
                found_dirs.append((list(cwd), dir_size))
            
            found_dirs.extend(find_directory_with_max_size(tree[fs_obj], size_max, cwd))

    return found_dirs


TREE = {"/": {}}

with open(os.path.dirname(__file__) + "/input.txt") as fp:
    data = fp.readlines()

interpreter = PromptInterpreter()

for i, l in enumerate(data):
    output = ""

    if l.startswith("$"):
        last_cmd = interpreter.current_cmd

        if last_cmd:
            cmd, cmd_output = interpreter.on_cmd_end()
            
            if type(cmd) is ListDirectoryCommand:
                update_tree_using_cmd_output(TREE, interpreter, cmd_output)
                
        interpreter.process_cmd(l[1:].strip())
    else:
        interpreter.receive_output(l)


cmd, cmd_output = interpreter.on_cmd_end()
if type(cmd) is ListDirectoryCommand:
    update_tree_using_cmd_output(TREE, interpreter, cmd_output)

global_size = get_size_directory(TREE)
small_dirs_size = find_directory_with_max_size(TREE, 100000)

total_small_dirs_size = sum(map(lambda d: d[1], small_dirs_size))

print(f"{total_small_dirs_size=}")


def get_all_folders(tree):
    if cwd == None:
        cwd = []

    found_dirs = []

    for fs_obj in tree:
        cwd.append(fs_obj)
        if type(tree[fs_obj]) == dict:
            dir_size = get_size_directory(tree[fs_obj])

            if dir_size <= size_max:
                found_dirs.append((list(cwd), dir_size))
            
            found_dirs.extend(find_directory_with_max_size(tree[fs_obj], size_max, cwd))

    return found_dirs