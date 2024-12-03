import os 
import sys
sys.path.insert(0,"/Users/zlawrence/Documents/LocalWorkArea/Advent-Of-Code-2024")
from shared.common import read_file
import re


def find_mult(lines):
    pattern = r"mul\(([0-9]{0,3}),([0-9]{0,3})\)"
    total = 0
    for line in lines:
        matches = re.findall(pattern,line)
        for match in matches:
            total += int(match[0])*int(match[1])
    return total
        
def remove_donts(lines):
    pattern = r"don't\([^)]*\).*?do\([^)]*\)"
    cleaned = []
    for line in lines:
        line = re.sub(pattern,"",line)
        if line.find("don't()"):
            line = re.sub(r"don't\([^)]*\).*?","",line)
        cleaned.append(line)
    return cleaned
        

def main(Test:bool=False):
    path = "Day3/test.txt" if Test else "Day3/input.txt"
    file = read_file(path)
    file = [line.strip() for line in file]
    file = ["".join(file)]
    total = find_mult(file)
    print(f"Part 1: {total}")
    print(f"Part 2: {find_mult(remove_donts(file))}")

if __name__ == "__main__":
    main()