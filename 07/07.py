COMMANDS = {}
TREE = {}
CWD = []


def register_cmd(*args):
    def wrapper(func):
        if func.name not in COMMANDS:
            COMMANDS[func.name] = func
        return func
    return wrapper


@register_cmd('cd')
class ChangeDirectoryCommand:
    output = ""

    def check(self, args):
        return len(args) >= 1
        
    def run(self, args):
        global CWD
        fs_obj = args[0]
        if fs_obj == "..":
            CWD = CWD[:-1]
        else:
            CWD.append(fs_obj)


@register_cmd('ls')
class ListDirectoryCommand:
    output = ""

    def check(self, args):
        return len(args) >= 1
        
    def run(self, args):
        global CWD
        fs_obj = args[0]
        if fs_obj == "..":
            CWD = CWD[:-1]
        else:
            CWD.append(fs_obj)
    
    def on_end():
        


class PromptInterpreter:
    def __init__(self):
        self.current_cmd = None

    def process_cmd(prompt: str):
        words = prompt.split(" ")
        cmd_name, args = words[0].strip(), list(map(str.strip, words[1:]))
        cmd_class = COMMANDS.get(cmd_name, None)
        
        if not cmd_class:
            raise Exception(f"Error: Command {cmd_name} not found!")
        
        cmd_obj = cmd_class()
        self.current_cmd = cmd_obj
        
        if not cmd_obj.check(args):
            raise Exception(f"Error while parsing command {cmd_obj.name}")
        
        cmd_obj.run(args)
        print(CWD)


with open("input.txt") as fp:
    data = fp.readlines()

interpreter = PromptInterpreter()

for l in data:
    output = ""
    if l.startswith("$"):
        interpreter.process_cmd(l[2:])
    else:
        output.append(l)

print(COMMANDS)
