import sys
sys.path.insert(0,"/Users/zlawrence/Documents/LocalWorkArea/Advent-Of-Code-2024")
from shared.common import read_file

def parse_input(path):
    diskmap = []
    file = read_file(path)
    for line in file:
        line = line.strip()
        line = list(line)
        file_key = 0
        for idx, value in enumerate(line):
            content = {
                "type":"file" if idx%2 == 0 else "space",
                "length":int(value),
                "id":file_key
            }
            file_key += 1 if idx%2 else 0
            diskmap.append(content)
    return diskmap

def rep_diskmap(diskmap):
    rep = []
    for content in diskmap:
        for i in range(content["length"]):
            rep.append(str(content["id"]) if content["type"] == "file" else ".")
    return rep 

def rep_diskmap_blocks(diskmap):
    rep = []
    for content in diskmap:
        block = []
        for i in range(content["length"]):
            block.append(str(content["id"]) if content["type"] == "file" else ".")
        if len(block) > 0:
            rep.append(block)
    return rep 

def reorder(diskmap):
    rep = rep_diskmap(diskmap)
    for idx in reversed(range(len(rep))):
        if rep[idx] == ".":
            continue
        first_index = rep.index('.')
        if first_index >= idx:
            break
        rep[idx],rep[first_index] = rep[first_index],rep[idx]
    return rep   

def dot_count(sublist):
    return sum(1 for item in sublist if item == '.')

def first_space(data,length):
    for i,sublist in enumerate(data):
        if any(item == '.' for item in sublist) and dot_count(sublist) >= length:
            return i
    else:
        return -1
    
def reorder_blocks(diskmap):
    rep = rep_diskmap_blocks(diskmap)
    for idx in reversed(range(len(rep))):
        sublist = rep[idx]
        if any(item == "." for item in sublist):
            continue
        length = len(sublist)
        first_index = first_space(rep,length)
        if first_index == -1:
            continue
        if first_index > idx:
            continue
        for j in range(len(sublist)):
            space = rep[first_index].index('.')
            rep[idx][j],rep[first_index][space] =  rep[first_index][space],rep[idx][j]
    return rep

def flatten(data):
    return [item for sublist in data for item in sublist]

def value(rep):
    value = [idx*int(val) for idx,val in enumerate(rep) if val != '.']
    return sum(value)

def part1(path):
    diskmap = parse_input(path)
    rep = reorder(diskmap)
    print(f"Part 1: {value(rep)}")
    
def part2(path):
    diskmap = parse_input(path)
    rep = flatten(reorder_blocks(diskmap))
    print(f"Part 2: {value(rep)}")

def main(day:int,Test:bool=False):
    path = f"Day{day}/test.txt" if Test else f"Day{day}/input.txt"
    part1(path)
    part2(path)

if __name__ == "__main__":
    main(9)