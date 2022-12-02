import os
 
# Part 01
fp = open(os.path.dirname(__file__) + "/input.txt")
data = fp.readlines()
fp.close()

calories_by_elf = []
calories_for_curr_elf = 0

for i, line in enumerate(data):
    line = line.strip()
    
    if len(line) > 0:
        calories_for_curr_elf += int(line)
    
    if len(line) == 0 or i == len(data)-1:
        calories_by_elf.append(calories_for_curr_elf)
        calories_for_curr_elf = 0

print(f"Max calories for any elf: {max(calories_by_elf)}")


# Part 02
print(f"Calories carried by the top 3 elves : {sum(sorted(calories_by_elf, reverse=True)[:3])}")