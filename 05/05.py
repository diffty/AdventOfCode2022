import re
import os
from typing import List


fp = open(os.path.dirname(__file__) + "/input.txt")
data = fp.readlines()
fp.close()

stacks: List[list] = []


for l in data:
    if l:
        res = re.findall(r"\[([A-Z])\]|(    )|move (\d+) from (\d+) to (\d+)", l, re.I)

        for i, match in enumerate(res):
            if match[0] or match[1]:
                if len(stacks) == i:
                    stacks.append([])

                if match[0]:
                    stacks[i].insert(0, match[0])

            elif all(match[2:]):
                crates_amount, stack_src, stack_dst = map(int, match[2:])
                stack_size = len(stacks[stack_src-1])
                stacks[stack_dst-1].extend(reversed(stacks[stack_src-1][stack_size-crates_amount:]))
                stacks[stack_src-1] = stacks[stack_src-1][:stack_size-crates_amount]
        
print("".join(map(lambda s: s[-1] if s else "", stacks)))