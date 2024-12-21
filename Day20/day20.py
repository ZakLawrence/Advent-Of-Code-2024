import sys
sys.path.insert(0,"/Users/zlawrence/Documents/LocalWorkArea/Advent-Of-Code-2024")
from shared.common import read_file
from collections import defaultdict
import heapq
from tqdm.auto import tqdm

class Graph(object):
    def __init__(self,connections, directed = False):
        self._graph = defaultdict(dict)
        self._directed = directed
        self.add_connections(connections)

    def add_connections(self,connections):
        for node1, node2, weight in connections:
            self.add(node1,node2,weight)

    def add(self,node1,node2,weight):
        self._graph[node1][node2] = weight
        if not self._directed:
            self._graph[node2][node1] = weight
    
    def remove(self,node):
        for n,cxns in self._graph.items():
            cxns.pop(node,None)
        self._graph.pop(node,None)

    def remove_connection(self, node1, node2):
        if node1 in self._graph and node2 in self._graph[node1]:
            del self._graph[node1][node2]  
            if not self._directed and node2 in self._graph and node1 in self._graph[node2]:
                del self._graph[node2][node1] 
        else:
            raise ValueError(f"No connection exists between {node1} and {node2}")

    def is_connected(self,node1,node2):
        return node1 in self._graph and node2 in self._graph[node1]
    
    def get_weight(self,node1,node2):
        return self._graph[node1].get(node2,None)
    
    def local_graph(self,node1):
        if node1 in self._graph:
            return self._graph[node1]
        else:
            raise ValueError(f"Cannot find node {node1} in graph!")
    
    def update_weight(self,node1,node2,weight):
        if node1 in self._graph and node2 in self._graph[node1]:
            self._graph[node1][node2] = weight
            if not self._directed:
                self._graph[node2][node1] = weight
        else: 
            raise ValueError(f"No edge between {node1} and {node2}")

    def find_path_length(self,start,end):
        if start not in self._graph or end not in self._graph:
            return False,float('inf')

        queue = [(0,start)]
        visited = set()
        distance = {start:0}

        while queue:
            current_distance, current_node = heapq.heappop(queue)
            if current_node in visited:
                continue
            visited.add(current_node)

            if current_node == end:
                return True,current_distance
            
            for neighbour, weight in self._graph[current_node].items():
                if neighbour not in visited:
                    new_distance = current_distance+weight
                    if new_distance < distance.get(neighbour,float('inf')):
                        distance[neighbour] = new_distance
                        heapq.heappush(queue,(new_distance,neighbour))
        return False, float('inf')

    def has_path(self, start, end):
        exists, _ = self.find_path_length(start, end)
        return exists

    def __str__(self):
        """Pretty-print the graph structure."""
        return str(dict(self._graph))
            
class RaceTrack(Graph):
    def __init__(self, start, end, connections, walls, spaces,Nrows,Ncols, directed=False):
        super().__init__(connections, directed)
        self.start = start
        self.end = end
        self.walls = walls
        self.spaces = spaces
        self.Nrows,self.Ncols = Nrows,Ncols

    def cheat_races(self,radius=2):
        original_route = self.Dijkstra()
        original_time = len(original_route)
        good_cheats = 0

        def get_positions(start, radius):
            spaces = set(self.spaces)
            x,y = start[0],start[1]
            positions_by_steps = {s:set() for s in range(2,radius+1)}
            for s in range(2,radius+1):
                for dx in range(-s,s+1):
                    dy = s - abs(dx)
                    npos = (x+dx,y+dy)
                    if npos in spaces:
                        positions_by_steps[s].add(npos)
                    npos = (x+dx,y-dy)
                    if npos in spaces and dy != 0:
                        positions_by_steps[s].add(npos)
            return positions_by_steps

        for space in tqdm(self.spaces):
            _,time = self.find_path_length(space,self.end)
            cheat_positions = get_positions(space,radius)
            for r in range(2,radius+1):
                cheats = [(space,cheat,r) for cheat in cheat_positions[r] if self.find_path_length(space,cheat)[1] > r]
                if not cheats:
                    continue
                for cheat in cheats:
                    self.add(cheat[0],cheat[1],cheat[2])
                    _,new_time = self.find_path_length(space,self.end)
                    savings = abs(time - new_time)
                    if savings >= 100:
                        good_cheats += 1
                    self.remove_connection(cheat[0],cheat[1])
            self.remove(space)
        return good_cheats

    def show_route(self,route):
        string = []
        for r in range(self.Nrows):
            for c in range(self.Ncols):
                pos = (r,c)
                if pos in self.walls:
                    string.append("\033[34m#\033[0m")
                elif pos == self.start:
                    string.append("\033[1;33mS\033[0m")
                elif pos == self.end:
                    string.append("\033[1;33mE\033[0m")
                elif pos in route:
                    string.append("\033[1;33m*\033[0m")
                else:
                    string.append(" ")
            string.append("\n")
        return "".join(string)

    def __str__(self):
        string = []
        for r in range(self.Nrows):
            for c in range(self.Ncols):
                pos = (r,c)
                if pos in self.walls:
                    string.append("\033[34m#\033[0m")
                elif pos == self.start:
                    string.append("S")
                elif pos == self.end:
                    string.append("E")
                else:
                    string.append(" ")
            string.append("\n")
        return "".join(string)
    

def parse_input(path):
    file = read_file(path)
    walls = set()
    spaces = set()
    start = None 
    end = None 
    for i,line in enumerate(file):
        line = line.strip()
        for j, char in enumerate(line):
            if char == "#":
                walls.add((i,j))
            else:
                spaces.add((i,j))
                if char == "S":
                    start = (i,j)
                if char == "E":
                    end = (i,j)
    Nrows,Ncols = i+1,j+1
    conections = set()

    ordered_spaces = []
    queue = [start]
    visited = set()
    visited.add(start)

    while queue:
        pos = queue.pop(0)
        ordered_spaces.append(pos)
        for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            npos = (pos[0]+dx,pos[1]+dy)
            if npos in spaces and npos not in visited:
                visited.add(npos)
                queue.append(npos)


    for i in range(len(ordered_spaces)-1):
        conections.add((ordered_spaces[i], ordered_spaces[i+1],1))
    
    return start,end,conections,walls,ordered_spaces,Nrows,Ncols


def part1(path):
    start,end,connections,walls, spaces,Nrows,Ncols = parse_input(path)
    track = RaceTrack(start,end,connections,walls,spaces,Nrows,Ncols)
    savings = track.cheat_races()
    print(f"Part 1: {savings}")
    #print(savings)

def part2(path):
    start,end,connections,walls, spaces,Nrows,Ncols = parse_input(path)
    track = RaceTrack(start,end,connections,walls,spaces,Nrows,Ncols)
    savings = track.cheat_races(20)
    print(f"Part 2: {savings}")
    #print(savings)


def main(day:int,Test:bool=False):
    path = f"Day{day}/test.txt" if Test else f"Day{day}/input.txt"
    #part1(path)
    part2(path)
    

if __name__ == "__main__":
    main(20)