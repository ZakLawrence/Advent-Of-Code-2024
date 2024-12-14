import sys
sys.path.insert(0,"/Users/zlawrence/Documents/LocalWorkArea/Advent-Of-Code-2024")
from shared.common import read_file
import numpy as np 
from numpy.linalg import inv
from math import isclose


def read_blocks(file):
    while True:
        block = [file.readline().strip() for _ in range(3)]
        if not any(block):
            break
        yield block
        file.readline()

def parse_input(file):
    matricies = []
    prizes = []

    def button_numbers(line):
        line = line.split(":")[1].strip()
        x,y = line.split(",")
        x=int(x.split("+")[1])
        y=int(y.split("+")[1])
        return x,y
    
    def prize_numbers(line):
        line = line.split(":")[1].strip()
        x,y = line.split(",")
        x=int(x.split('=')[1]) 
        y=int(y.split('=')[1]) 
        return x,y


    for block in read_blocks(file):
        Ax,Ay = button_numbers(block[0])
        Bx,By = button_numbers(block[1])
        Px,Py = prize_numbers(block[2])
        
        matrix = np.matrix([[Ax,Bx],[Ay,By]],dtype=int)
        matricies.append(matrix)
        prize = np.matrix([[Px],[Py]],dtype=int)
        prizes.append(prize)
    
    return matricies,prizes

def find_prizes(matricies, prizes):
    cost = 0
    for matrix, prize in zip(matricies,prizes):
        mults = np.linalg.solve(matrix, prize)
        a, b = mults.flatten().A[0]  # Extract the two solutions
        if a >= 0 and b >= 0:
            diff_a = abs(a-round(a))
            diff_b = abs(b-round(b))
            if diff_a < 1e-4 and diff_b < 1e-4:
                cost += a*3 + b*1
    return cost

def correct_prizes(prizes):
    for i in range(len(prizes)):
        prizes[i][0] = 10000000000000 +  prizes[i][0]
        prizes[i][1] = 10000000000000 +  prizes[i][1]
    return prizes

def part1(path):
    file = read_file(path)
    matricies, prizes = parse_input(file)
    cost = find_prizes(matricies,prizes)
    print(f"Part 1: {cost}")

def part2(path):
    file = read_file(path)
    matricies, prizes = parse_input(file)
    prizes = correct_prizes(prizes)
    cost = find_prizes(matricies,prizes)
    print(f"Part 2: {cost}")


def main(day:int,Test:bool=False):
    path = f"Day{day}/test.txt" if Test else f"Day{day}/input.txt"
    part1(path)
    part2(path)

if __name__ == "__main__":
    main(13)