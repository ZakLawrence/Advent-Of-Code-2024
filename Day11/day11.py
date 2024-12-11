import sys
sys.path.insert(0,"/Users/zlawrence/Documents/LocalWorkArea/Advent-Of-Code-2024")
from shared.common import read_file
from tqdm.auto import tqdm
import numpy as np
from math import ceil

def get_stones(path):
    file = read_file(path)
    stones = file.readlines()[0].strip()
    stones = [int(stone) for stone in stones.split(' ') if stone]
    return stones

def rules(value):
    if value == 0: 
        return [1]
    elif len(str(value))%2 == 0:
        ndigits = int(len(str(value))/2)
        return [int(str(value)[:ndigits]),int(str(value)[ndigits:])]
    else:
        return [value*2024] 

def part1(stones):    
    lenghts = [len(stones)]
    for i in range(25):
        stones = [item for stone in stones for item in rules(stone)]
        lenghts.append(len(stones))
    return lenghts, stones
    
def part2(stones):
    keys = set(stones)
    stones = np.array(stones)
    stones = {
        key: len(stones[stones==key]) for key in keys 
    }
    for i in range(50):
        new_stones = {}
        keys = stones.keys()
        for key in keys:
            tot = stones[key]
            for nk in rules(key):
                if nk in new_stones.keys():
                    new_stones[nk] += tot
                else:
                    new_stones[nk] = tot
        stones = new_stones
    total = sum(item for key,item in stones.items())
    print(f"Part 2: {total}")
        
def main(day:int,Test:bool=False):
    path = f"Day{day}/test.txt" if Test else f"Day{day}/input.txt"
    stones = get_stones(path)   
    lengths, stones = part1(stones)
    print(f"Part 1: {lengths[-1]}")
    part2(stones)

if __name__ == "__main__":
    main(11)