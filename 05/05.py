import re
import os


with open(os.path.dirname(__file__) + "/input.txt") as fp:
    data = fp.readlines()

# Part 01
stacks = []

for l in data:
    if l:
        res = re.findall(r"\[([A-Z])\]|(    )|move (\d+) from (\d+) to (\d+)", l, re.I)

        for i, match in enumerate(res):
            if match[0] or match[1]:
                if len(stacks) == i:
                    stacks.append("")

                if match[0]:
                    stacks[i] = f"{match[0]}{stacks[i]}"

            elif all(match[2:]):
                crates_amount, stack_src, stack_dst = map(int, match[2:])
                stack_size = len(stacks[stack_src-1])
                stacks[stack_dst-1] = f"{stacks[stack_dst-1]}{stacks[stack_src-1][stack_size-crates_amount:][::-1]}"
                stacks[stack_src-1] = stacks[stack_src-1][:stack_size-crates_amount]

print("".join(map(lambda s: s[-1] if s else "", stacks)))