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

    def remove_wall(self,position):
        if position in self.walls:
            neigbours = self._graph[position].keys()
            for neighbour in neigbours:
                self.update_weight(position,neighbour,1)
            self.walls.remove(position)
        else:
            raise ValueError(f"Can't remove wall at position {position}! Not a wall!")
    
    def add_wall(self,position):
        if position not in self.walls:
            neigbours = self._graph[position].keys()
            for neighbour in neigbours:
                self.update_weight(position,neighbour,float('inf'))
            self.walls.add(position)
        else:
            raise ValueError(f"Can't add wall at position {position}! Already a wall!")

    def cheat_races(self):
        directions = [(0,1),(0,-1),(1,0),(-1,0)]
        cheat_walls = set()
        for (px,py) in self.spaces:
            for (dx,dy) in directions:
                npos = (px+dx,py+dy)
                npos_2 = (px+2*dx,py+2*dy)
                if npos in self.walls and npos_2 in self.spaces:
                    cheat_walls.add(npos)
        original_route = self.Dijkstra()
        original_time = len(original_route)
        savings = dict()
        for cheat_wall in tqdm(cheat_walls):
            self.remove_wall(cheat_wall)
            new_time = len(self.Dijkstra())
            delta = abs(new_time-original_time)
            savings[cheat_wall] = delta
            self.add_wall(cheat_wall)
        optimal = [wall for wall,time in savings.items() if time >= 100]

        return savings,optimal


    def Dijkstra(self):
        start,end = self.start,self.end
        graph = self._graph
        dist = {v:float("inf") for v in graph.keys()}
        previous = {v:None for v in graph.keys()}
        dist[start] = 0
        
        queue = [(dist[v],v) for v in graph.keys()]
        heapq.heapify(queue)

        def route(target,previous):
            path = []
            current = target
            while current in previous:
                path.append(current)
                current = previous[current]
            return path[::-1]

        while queue:
            _, node = heapq.heappop(queue)
                
            for neighbour in graph[node].keys():
                cost = dist[node]+graph[node][neighbour]
                if cost < dist[neighbour]:
                    dist[neighbour] = cost
                    previous[neighbour] = node
                    heapq.heappush(queue,(cost,neighbour))
        return route(end,previous)

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
    End = None 
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

    directions = [(0,1),(0,-1),(1,0),(-1,0)]
    conections = set()
    for r in range(Nrows):
        for c in range(Ncols):
            for dr,dc in directions:
                npos = (r+dr,c+dc)
                if npos in walls or (r,c) in walls:
                    conections.add(((r,c),npos,float('inf')))
                else:
                    conections.add(((r,c),npos,1))
    return start,end,conections,walls,spaces,Nrows,Ncols


def part1(path):
    start,end,connections,walls, spaces,Nrows,Ncols = parse_input(path)
    track = RaceTrack(start,end,connections,walls,spaces,Nrows,Ncols)
    route = track.Dijkstra()
    print(track.show_route(route))

    savings, optimal = track.cheat_races()
    print(f"Part 1: {len(optimal)}")
    print(savings)


def main(day:int,Test:bool=False):
    path = f"Day{day}/test.txt" if Test else f"Day{day}/input.txt"
    part1(path)
    

if __name__ == "__main__":
    main(20)