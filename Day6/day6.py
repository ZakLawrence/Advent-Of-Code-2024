import sys
sys.path.insert(0,"/Users/zlawrence/Documents/LocalWorkArea/Advent-Of-Code-2024")
from shared.common import read_file
import re
from tqdm.auto import tqdm
from concurrent.futures import ThreadPoolExecutor


class room:
    def __init__(self,path) -> None:
        file = read_file(path)

        self.obsticles = []
        self.guard_start = None
        for row,line in enumerate(file):
            line = line.strip()
            cols = len(line)
            obsticles = [m.start() for m in re.finditer('#',line)]
            for obsticle in obsticles:
                self.obsticles.append((row,obsticle))
            if line.find("^") != -1:
                self.guard = guard(row,line.find("^"))    
                self.guard_start = (row,line.find("^"))
        self.Nrows = row+1
        self.Ncols = cols

    def __str__(self) -> str:
        return f"Grid({self.Nrows}x{self.Ncols}), Obsticles({self.obsticles}), Guard({self.guard})"

    def set_obsticles(self,obsticles):
        self.obsticles = obsticles

    def run_timelines(self):
        loops = []
        visited = set([item[0] for item in self.guard.previous_positions])
        self.guard.reset()
        obsticles = self.obsticles
        for pos in tqdm(visited):
                temp_obsticles = obsticles.copy()
                temp_obsticles.append(pos)
                self.set_obsticles(temp_obsticles)
                self.run_route()
                loops.append(self.guard.in_loop())
                self.guard.reset()
                self.set_obsticles(obsticles)
        return sum(loops)

    def run_route(self):
        while self.guard.moveable(self.Nrows,self.Ncols):
            #print(self.guard)
            if self.guard.next_position() in self.obsticles:
                self.guard.rotate()
            else:
                self.guard.step() 
        return self.guard.len_route()

class guard:
    def __init__(self,row,col) -> None:
        self.current_position = (row,col)
        self.start = (row,col)
        self.delta = (-1,0)
        self.previous_positions = []

    def __str__(self) -> str:
        return f"{self.current_position}"

    def position(self):
        return self.current_position
    
    def len_route(self):
        pos = [item[0] for item in self.previous_positions]
        return len(set(pos))

    def next_position(self):
        return tuple(sum(x) for x in zip(self.current_position,self.delta))

    def in_room(self,Nrows,Ncols):
        current_col, current_row = self.current_position
        if 0 <= current_col < Ncols and 0 <= current_row < Nrows:
            return True
        return False

    def in_loop(self):
        current_pos = (self.current_position,self.delta)
        if current_pos in self.previous_positions:
            return True
        return False

    def moveable(self,Nrows,Ncols):
        if not self.in_room(Nrows,Ncols):
            return False
        elif self.in_loop():
            return False
        else:
            return True

    def step(self): 
        self.previous_positions.append((self.current_position,self.delta))
        self.current_position = self.next_position()
    
    def rotate(self):
        delta = complex(*self.delta)
        delta = -1j*delta
        self.delta = (int(delta.real),int(delta.imag))
    
    def reset(self):
        self.current_position = self.start
        self.delta = (-1,0)
        self.previous_positions = []

def main(Test:bool=False):
    path = "Day6/test.txt" if Test else "Day6/input.txt"
    grid = room(path)
    route = grid.run_route()
    print(f"Part 1: {route}")
    loops = grid.run_timelines()
    print(f"Part 2: {loops}")

if __name__ == "__main__":
    main()