import sys
sys.path.insert(0,"/Users/zlawrence/Documents/LocalWorkArea/Advent-Of-Code-2024")
from shared.common import read_file

numpad = {
    '7':(0,0),
    '8':(0,1),
    '9':(0,2),
    '4':(1,0),
    '5':(1,1),
    '6':(1,2),
    '1':(2,0),
    '2':(2,1),
    '3':(2,2),
    '0':(3,1),
    'A':(3,2)
}

dirpad = {
    '^':(0,1),
    'A':(0,2),
    '<':(1,0),
    'v':(1,1),
    '>':(1,2)
}

cache = {}

def generate_movement(keypad,start,end):
    start_position = keypad[start]
    to_check = [(start_position,'')]
    target = keypad[end]
    while to_check:
        current_position, path = to_check.pop()
        if current_position == target:
            yield path
            continue
        dx,dy = target[0]-current_position[0],target[1]-current_position[1]
        if dx != 0:
            npos = current_position[0]+(dx//abs(dx)),current_position[1]
            if npos in keypad.values():
                if dx > 0:
                    to_check.append((npos,path+'v'))
                elif dx < 0:
                    to_check.append((npos,path+'^'))
        if dy != 0:
            npos = current_position[0],current_position[1]+(dy//abs(dy))
            if npos in keypad.values():
                if dy > 0:
                    to_check.append((npos,path+'>'))
                elif dy < 0:
                    to_check.append((npos,path+'<'))
    

def get_minimum_code(keypad,code,robots=3):
    if (len(keypad),code,robots) in cache:
        return cache[(len(keypad),code,robots)]
    if robots == 0:
        cache[(len(keypad),code,robots)] = len(code)
        return len(code)
    
    start = 'A'
    min_code_length = 0
    new_robots = robots - 1
    for char in code:
        min_code_length += min(
            get_minimum_code(dirpad,sequence+'A',new_robots) for sequence in generate_movement(keypad,start,char)
        )
        start = char
    cache[(len(keypad),code,robots)] = min_code_length
    return min_code_length

def get_codes(path):
    file = read_file(path)
    codes = []
    for line in file:
        codes.append(line.strip())
    return codes

def part1(path):
    codes = get_codes(path)
    result = 0
    for code in codes:
        min_code = get_minimum_code(numpad,code)
        result += min_code * int(''.join(c for c in code if c in '0123456789'))
    print(f"Part 1: {result}")

def part2(path):
    codes = get_codes(path)
    result = 0
    for code in codes:
        min_code = get_minimum_code(numpad,code,26)
        result += min_code * int(''.join(c for c in code if c in '0123456789'))
    print(f"Part 1: {result}")


def main(day:int,Test:bool=False):
    path = f"Day{day}/test.txt" if Test else f"Day{day}/input.txt"
    part1(path)
    part2(path)

if __name__ == "__main__":
    main(21)