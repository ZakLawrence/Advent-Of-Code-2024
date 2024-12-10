import sys
sys.path.insert(0,"/Users/zlawrence/Documents/LocalWorkArea/Advent-Of-Code-2024")
from shared.common import read_file

def get_nodes(grid,value):
    return [(i,j) for i in range(len(grid)) for j in range(len(grid[i])) if grid[i][j] == value]

def routes(grid,starts):
    directions = [(0,1),(0,-1),(1,0),(-1,0)] 
    Nx,Ny = len(grid),len(grid[0])
    def step_1(h,pos,found):
        cx,cy = pos
        if grid[cx][cy] == 9:
            found.add(pos)
            return found
        for delta in directions:
            dx,dy = delta
            x,y = cx+dx,cy+dy
            if 0 <= x < Nx and 0 <= cy+dy < Ny:
                if grid[x][y] == h + 1:
                    found.union(step_1(h+1,(x,y),found))
        return found
    
    def step_2(h,pos):
        cx,cy = pos
        rank = 0
        if grid[cx][cy] == 9:
            return 1
        for delta in directions:
            dx,dy = delta
            x,y = cx+dx,cy+dy
            if 0 <= x < Nx and 0 <= cy+dy < Ny:
                if grid[x][y] == h + 1:
                    rank += step_2(h+1,(x,y))
        return rank
    
    return sum(len(step_1(0,start,set())) for start in starts), sum(step_2(0,start) for start in starts)
        
def parse_file(file):
    locations =[]
    for line in file:
        line = line.strip()
        locations.append(list(map(int,line)))
    return locations

def part1(path):
    file = read_file(path)
    locations = parse_file(file)
    trail_heads = get_nodes(locations,0)
    print(f"Part 1: {routes(locations,trail_heads)}")

def main(day:int,Test:bool=False):
    path = f"Day{day}/test.txt" if Test else f"Day{day}/input.txt"
    part1(path)

if __name__ == "__main__":
    main(10)