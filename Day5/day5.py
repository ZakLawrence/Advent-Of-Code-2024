import sys
sys.path.insert(0,"/Users/zlawrence/Documents/LocalWorkArea/Advent-Of-Code-2024")
from shared.common import read_file
import math

def add_rule(dic,key,value):
    if key in dic:
        dic[key].append(value)
    else:
        dic[key] = [value]
    return dic

def parse_input(lines):
    rules = {}
    printings = []
    for line in lines: 
        line = line.strip()
        if line.find("|") != -1:
            key, page = line.split("|")
            rules = add_rule(rules,key,page)
        if line.find(",") != -1:
            printings.append(line.split(","))
    return rules, printings

def check_printing(rules, prinitng):
    for i in range(len(prinitng)):
        elem = prinitng[i]
        if elem not in rules:
            continue 
        rule = rules[elem]
        part = prinitng[0:i+1]
        check = any(x in part for x in rule)
        if check:
            return False
    return True

def part1(path):
    file = read_file(path)
    rules, printings = parse_input(file)
    total = 0
    for printing in printings:
        check = check_printing(rules,printing)
        if check:
            mid = math.ceil((len(printing)-1)/2)
            total += int(printing[mid])
    print(f"Part 1: {total}")

def fix_printing(rules,printing):
    for n in range(len(printing)-1,0,-1):
        for i in range(n):
            rule = [] if printing[i+1] not in rules else rules[printing[i+1]]
            if printing[i] in rule: 
                printing[i], printing[i+1] = printing[i+1],printing[i]
    return printing

def part2(path):
    file = read_file(path)
    rules, printings = parse_input(file)
    total = 0
    for printing in printings:
        check = check_printing(rules,printing)
        if not check:
            printing = fix_printing(rules,printing)
            mid = math.ceil((len(printing)-1)/2)
            total += int(printing[mid])
    print(f"Part 2: {total}")

def main(Test:bool=False):
    path = "Day5/test.txt" if Test else "Day5/input.txt"
    part1(path)
    part2(path)

if __name__ == "__main__":
    main()