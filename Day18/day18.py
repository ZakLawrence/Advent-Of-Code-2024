import sys
sys.path.insert(0,"/Users/zlawrence/Documents/LocalWorkArea/Advent-Of-Code-2024")
from shared.common import read_file
from collections import defaultdict
import heapq
from tqdm.auto import tqdm

class Graph(object):
    def __init__(self,connections, directed = False):
        self._graph = defaultdict(set)
        self._directed = directed
        self.add_connections(connections)

    def add_connections(self,connections):
        for node1, node2 in connections:
            self.add(node1,node2)

    def add(self,node1,node2):
        self._graph[node1].add(node2)
        if not self._directed:
            self._graph[node2].add(node1)
    
    def remove(self,node):
        for n,cxns in self._graph.items():
            try:
                cxns.remove(node)
            except KeyError:
                pass
        try: 
            del self._graph[node]
        except KeyError:
            pass
    
    def is_connected(self,node1,node2):
        return node1 in self._graph and node2 in self._graph[node1]

class memory(Graph):
    def __init__(self, path,bits,Test=False):
        self.min_bits = bits
        self.parse_inputs(path)
        connections = self.build_graph(bits,Test)
        super().__init__(connections)
    
    def increment_bits(self,Test):
        for bit in tqdm(range(self.min_bits,len(self.corrupted_memory))):
            connections = self.build_graph(bit,Test)
            super().__init__(connections)
            route = self.Dijkstra()
            if self.start not in route or self.end not in route:
                return bit

    def parse_inputs(self,path):
        file = read_file(path)
        corrupted_memory = []
        for line in file:
            line = line.strip()
            px,py = line.split(",")
            corrupted_memory.append((int(px),int(py)))
        self.corrupted_memory = corrupted_memory

    def build_graph(self,bits,Test):
        grid_size = 7 if Test else 71
        self.start = (0,0)
        self.end = (grid_size-1,grid_size-1)
        corrupted = [self.corrupted_memory[i] for i in range(bits)]
        
        spaces = [(i,j) for i in range(grid_size) for j in range(grid_size) if (i,j) not in corrupted]
        connections = set()
        
        directions = [(0,1),(0,-1),(1,0),(-1,0)] 
        for space in spaces:
            sx,sy = space
            for (dx,dy) in directions:
                neighbour = (sx+dx,sy+dy)
                if neighbour in spaces:
                    connections.add((space,neighbour))

        return list(connections)

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
                
            for neighbour in graph[node]:
                cost = dist[node]+1
                if cost < dist[neighbour]:
                    dist[neighbour] = cost
                    previous[neighbour] = node
                    heapq.heappush(queue,(cost,neighbour))
        return route(end,previous)

def part1(path,Test):
    bits = 12 if Test else 1024
    memeory_grid = memory(path,bits,Test)
    route = memeory_grid.Dijkstra()
    print(f"Part 1: {len(route)-1}")

def part2(path,Test):
    bits = 12 if Test else 1024
    memeory_grid = memory(path,bits,Test)
    bit = memeory_grid.increment_bits(Test)
    print(memeory_grid.corrupted_memory[bit-1])

def main(day:int,Test:bool=False):
    path = f"Day{day}/test.txt" if Test else f"Day{day}/input.txt"

    part1(path,Test)
    part2(path,Test)

if __name__ == "__main__":
    main(18)