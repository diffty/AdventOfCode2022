import os
import math

with open(os.path.dirname(__file__) + "/input.txt") as fp:
    data = list(map(str.strip, fp.readlines()))
    data_rot = list(zip(*data))
    size = (len(data[0]), len(data))
    size_rot = list(reversed(size))

def str_rshift(s):
    return s[0] + "".join(s) if s else ""

def build_visibility_map(line):
    def _build_visibility_map_side(line):
        line_max_height_map = [line[0]]
        line_max = max(line)
        
        first_char_max = line.index(line_max)

        for c in line[1:first_char_max+1]:
            line_max_height_map.append(c if c > line_max_height_map[-1] else line_max_height_map[-1])

        return line_max_height_map
    
    left_part = _build_visibility_map_side(line)
    right_part = list(reversed(_build_visibility_map_side(list(reversed(line)))[:-1]))
    
    line_size = len(line)
    highest_size = line_size-len(left_part)-len(right_part)

    final_left_part = str_rshift(left_part)
    pad_part = "".join([max(line)]*(line_size-(len(left_part)+1)-(len(right_part)+1)))
    final_right_part = "".join(reversed(str_rshift("".join((reversed(right_part)))))) if right_part else '0'

    if highest_size > 1:
        result = list(final_left_part + pad_part + final_right_part)
    elif highest_size == 1:
        result = list(final_left_part[:-1] + pad_part + final_right_part)
    else:
        result = list(final_left_part[:-2] + min(final_left_part[-1], final_right_part[0]) + final_right_part[1:])
    
    return result


visibility_per_tree = list(zip(sum([build_visibility_map(l) for l in data], []),
                               sum(list(map(list, zip(*[build_visibility_map(l) for l in data_rot]))), []),
                               "".join(data)))

results = list(map(lambda v: v[2] <= v[0] and v[2] <= v[1], visibility_per_tree))
visible_trees = size[0]*size[1] - sum(list(map(lambda y: sum(results[y*size[0]+1:(y+1)*size[0]-1]), range(1, size[1]-1))))
print(f"{visible_trees=}")
