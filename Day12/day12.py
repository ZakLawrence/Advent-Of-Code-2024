import sys
sys.path.insert(0,"/Users/zlawrence/Documents/LocalWorkArea/Advent-Of-Code-2024")
from shared.common import read_file

class region:
    def __init__(self,name,positions):
        self.name = name
        self.positions = positions
        self.regions = self.find_contiguous()
        self.cost1 = self.cost1()
        self.cost2 = self.cost2()
    
    def find_contiguous(self):
        positions = self.positions
        regions = []
        deltas = [(0,1),(0,-1),(1,0),(-1,0)]

        def connected(pos,found):
            px,py = pos
            found.add(pos)
            for (dx,dy) in deltas:
                nx,ny = px+dx,py+dy
                if (nx,ny) in positions:
                    found.add((nx,ny))
                    positions.remove((nx,ny))
                    found.union(connected((nx,ny),found))
            return found

        def fence(patch):
            perimiter = 0
            out_positions = set()
            for (px,py) in patch:
                for (dx,dy) in deltas:
                    nx,ny = px+dx,py+dy
                    if (nx,ny) not in patch:
                        perimiter += 1
                        out_positions.add(((nx,ny),(dx,dy)))
            return perimiter, out_positions
        
        def sides(out_positions):
            def conect(pos,found):
                px,py = pos
                for (dx,dy) in deltas:
                   nx,ny = px+dx,py+dy
                   if (nx,ny) in subset:
                       found.add((nx,ny))
                       subset.remove((nx,ny))
                       found.union(conect((nx,ny),found))
                return found


            Nsides = 0
            for delta in deltas:
                subset = [x[0] for x in out_positions if x[1] == delta]
                regions = []
                while len(subset) > 0:
                    pos, *subset = subset
                    side = conect(pos,set())
                    regions.append(side)
                Nsides += len(regions)
            return Nsides                    

        while len(positions) > 0:
            pos, *positions = positions
            patch= connected(pos,set())
            perimiter, out_positions = fence(patch)
            Nsides = sides(out_positions)
            regions.append((patch,perimiter,Nsides))
        return regions
    
    def cost1(self):
        cost = 0
        for patch,fence,sides in self.regions:
            cost += len(patch)*fence
        return cost
    
    def cost2(self):
        cost = 0
        for patch,fence,sides in self.regions:
            cost += len(patch)*sides
        return cost

def parse_file(path):
    file = read_file(path)
    regions = {}
    for i, line in enumerate(file):
        line = line.strip()
        split_line = list(line)
        for j, char in enumerate(split_line):
            if char in regions.keys():
                regions[char].append((i,j))
            else: 
                regions[char] = [(i,j)]
    return regions

def part1(path):
    proto_regions = parse_file(path)
    Price1 = 0
    Price2 = 0
    for key,positions in proto_regions.items():
        R = region(key,positions)
        Price1 += R.cost1
        Price2 += R.cost2
    print(f"Part 1: {Price1}")
    print(f"Part 2: {Price2}")



def main(day:int,Test:bool=False):
    path = f"Day{day}/test.txt" if Test else f"Day{day}/input.txt"
    part1(path)

if __name__ == "__main__":
    main(12)