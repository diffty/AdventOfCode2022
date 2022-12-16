import os
import math

with open(os.path.dirname(__file__) + "/input.txt") as fp:
    data = list(map(str.strip, fp.readlines()))
    data_rot = list(zip(*data))
    size = (len(data[0]), len(data))
    size_rot = list(reversed(size))

def build_visibility_map(line):
    def _build_visibility_map_side(line):
        line_max_height_map = [line[0]]
        line_max = max(line)
        first_char_max = line.index(line_max)

        for c in line[1:first_char_max+1]:
            line_max_height_map.append(c if c > line_max_height_map[-1] else line_max_height_map[-1])

        return line_max_height_map
    
    #left_part = _build_visibility_map_side(line)
    #right_part = list(reversed(_build_visibility_map_side(list(reversed(line)))[:-1]))
    #old_one = left_part + [left_part[-1]]*(len(line)-len(left_part)-len(right_part)) + right_part

    left_part = _build_visibility_map_side(line)
    padding_char = left_part[-1]
    left_part = [" "] + left_part[:-1]
    right_part = list(reversed(_build_visibility_map_side(list(reversed(line)))[:-2])) + [" "]
    return left_part + [padding_char]*(len(line)-len(left_part)-len(right_part)) + right_part

visibility_per_tree = list(zip(sum([build_visibility_map(l) for l in data], []),
                               sum([build_visibility_map(l) for l in data_rot], []),
                               "".join(data)))

print("\n".join(data))
print()
print("\n".join(["".join(build_visibility_map(l)) for l in data]))
print()
print(list(map(lambda v: v[2] <= v[0], visibility_per_tree)))
