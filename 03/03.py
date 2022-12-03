import os


PRIO_TABLE = list(map(lambda i: chr(97+i%26-int(i/26)*32), range(52)))


# Part 1
with open(os.path.dirname(__file__) + "/input.txt") as fp:
    data = fp.readlines()
    common_items = []

    for l in data:
        common_items.extend(set(filter(lambda c: c in l[int(len(l.strip())/2):],
                                l[:int(len(l.strip())/2)])))
        
    print(sum(map(lambda i: PRIO_TABLE.index(i)+1, common_items)))


# Part 2
with open(os.path.dirname(__file__) + "/input.txt") as fp:
    data = list(map(str.strip, fp.readlines()))
    common_items = []

    for grp_elves_items in list(map(lambda i: data[i:i+3], range(0, int(len(data)), 3))):
        common_items.extend(set(filter(lambda c: all(map(lambda i: c in grp_elves_items[i],
                                                         range(1, len(grp_elves_items)))),
                                       grp_elves_items[0])))

    print(sum(map(lambda i: PRIO_TABLE.index(i)+1, common_items)))
