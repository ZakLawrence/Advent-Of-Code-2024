import sys
sys.path.insert(0,"/Users/zlawrence/Documents/LocalWorkArea/Advent-Of-Code-2024")
from shared.common import read_file
import numpy as np

def make_grid(lines):
    grid = np.array([
        [elem for elem in line.strip()] for line in lines
    ])
    return grid

def get_elem(grid,r,c):
    Row, Col = grid.shape
    if 0 <= r < Row and 0 <= c < Col:
        return grid[r][c]
    else:
        return ''

def search(grid,row,col):
    if get_elem(grid,row,col) != "X":
        return 0 

    count = 0
    deltas = ((0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1),(-1,1),(-1,-1))    
    for delta_r,delta_c in deltas:
        r = row
        c = col
        for step in range(3):
            r += delta_r
            c += delta_c
            if get_elem(grid,r,c) != 'MAS'[step]:
                break
        else: 
            count += 1
    return count

def search_cross(grid,row,col):
    if get_elem(grid,row,col) != "A":
        return 0
    deltas = (((1,1),(-1,-1)),((-1,1),(1,-1)))
    x = 0
    for diag in deltas:
        d1,d2 = diag
        cross = get_elem(grid,row+d1[0],col+d1[1]) + get_elem(grid,row+d2[0],col+d2[1])
        if cross == 'MS' or cross == "SM":
            x +=1 
    return 1 if x==2 else 0

def total_xmas(grid):
    Row, Col = grid.shape
    total = sum(search(grid,r,c) for r in range(Row) for c in range(Col))
    return total

def total_cross_mass(grid):
    Row, Col = grid.shape
    total = sum(search_cross(grid,r,c) for r in range(Row) for c in range(Col))
    return total

def part1(grid):
    print(f"Part 1: {total_xmas(grid)}")
    
def part2(grid):
    print(f"Part 2: {total_cross_mass(grid)}")

def main(Test:bool=False):
    path = "Day4/test.txt" if Test else "Day4/input.txt"
    file = read_file(path)
    grid = make_grid(file)
    part1(grid)
    part2(grid)

if __name__ == "__main__":
    main()