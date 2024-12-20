import sys
sys.path.insert(0,"/Users/zlawrence/Documents/LocalWorkArea/Advent-Of-Code-2024")
from shared.common import read_file

def parse_input(path):
    file = read_file(path)
    designs = []
    for i,line in enumerate(file):
        line = line.strip()
        if not line:
            continue

        if i == 0: 
            patterns = {pattern.strip() for pattern in line.split(',')}
        else:
            designs.append(line)
    return patterns,designs

def check_design(design,patterns):
    in_design = {pattern for pattern in patterns if pattern in design}
    
    def can_construct_design(design, patterns):
        n = len(design)
        can_construct = [False] * (n + 1)  
        can_construct[0] = True

        for i in range(n + 1): 
            if not can_construct[i]:
                continue
            for pattern in patterns:
                plen = len(pattern)
                if design[i:i+plen] == pattern:
                    can_construct[i+plen] = True
                    
        return can_construct[n]
    
    possible = can_construct_design(design,in_design)    

    def number_solutions(design,patterns):
        n = len(design)
        num_constructions = [1] + [0]*n
        for i in range(1,len(num_constructions)):
            for pattern in patterns:
                plen = len(pattern)
                if plen > i:
                    continue
                if design[i-plen:i] == pattern:
                    num_constructions[i] += num_constructions[i-plen]
        return num_constructions[-1]

    combinations = number_solutions(design,patterns)

    return possible,combinations

def part1(path):
    patterns, designs = parse_input(path)
    valid = [check_design(design,patterns)[0] for design in designs]
    print(f"Part 1: {sum(valid)}")

def part2(path):
    patterns, designs = parse_input(path)
    valid = [check_design(design,patterns)[1] for design in designs]
    print(f"Part 2: {sum(valid)}")

def main(day:int,Test:bool=False):
    path = f"Day{day}/test.txt" if Test else f"Day{day}/input.txt"
    part1(path)
    part2(path)


if __name__ == "__main__":
    main(19)