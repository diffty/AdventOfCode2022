import os


with open(os.path.dirname(__file__) + "/input.txt") as fp:
    # Part 1
    data = list(map(str.strip, filter(lambda l: ',' in l, fp.readlines())))
    elf_pairs = map(lambda s: s.split(","), data)
    elf_assigns = map(lambda p: list(map(lambda e: list(range(int(e.split("-")[0]), int(e.split("-")[1])+1)), p)), elf_pairs)

    nb_doubles = list(map(lambda p: set(p[0]).issubset(p[1]) or set(p[0]).issuperset(p[1]), elf_assigns)).count(True)
    print(f"{nb_doubles=}")

    # Part 2
    nb_overlap = len(list(filter(lambda i: len(i) > 0, map(lambda p: set(p[0]) & set(p[1]), elf_assigns))))
    print(f"{nb_overlap=}")
