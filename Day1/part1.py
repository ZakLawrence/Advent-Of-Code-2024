import os 
import sys
sys.path.insert(0,"/Users/zlawrence/Documents/LocalWorkArea/Advent-Of-Code-2024")
from shared.common import read_file

def make_lists(lines):
    list_1 = [] 
    list_2 = []
    for line in lines:
        parts = [part for part in line.split(" ") if part]
        list_1.append(int(parts[0].strip()))
        list_2.append(int(parts[1].strip()))
    return list_1,list_2

def list_distance(list_1,list_2):
    list_1 = sorted(list_1)
    list_2 = sorted(list_2)
    distance = [abs(item1 - item2) for item1,item2 in zip(list_1,list_2)]
    return distance 

def list_similarity(list_1,list_2):
    list_1 = sorted(list_1)
    list_2 = sorted(list_2)
    def match(list,value):
        return [x for x in list if x == value]
    similarity = [x*len(match(list_2,x)) for x in list_1]
    return similarity



def main(Test:bool=False):
    path = "Day1/test.txt" if Test else "Day1/part1.txt"
    file = read_file(path)
    list_1, list_2 = make_lists(file)
    distance = list_distance(list_1,list_2)
    print(f"Part 1: {sum(distance)}")
    
    similarity = list_similarity(list_1,list_2)
    print(f"Part 2: {sum(similarity)}")


if __name__ == "__main__":
    main()