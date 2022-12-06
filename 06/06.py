import os


with open(os.path.dirname(__file__) + "/input.txt") as fp:
    data = fp.read().strip()


def find_stream_start(stream_data, nb_unique_chars):
    for cur in range(len(stream_data)):
        if len(set(stream_data[cur:cur+nb_unique_chars])) == nb_unique_chars:
            return cur+nb_unique_chars-1


print(find_stream_start(data, 4)+1)  # Part 1
print(find_stream_start(data, 14)+1) # Part 2
