import sys
sys.path.insert(0,"/Users/zlawrence/Documents/LocalWorkArea/Advent-Of-Code-2024")
from shared.common import read_file
import heapq
from collections import defaultdict

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
    

class maze(Graph):
    def __init__(self,path):
        self.start, self.end, self.space,self.rows,self.cols = self.build_maze(path)
        connections = self.build_connections()
        super(maze,self).__init__(connections)

    def __str__(self):
        string = []
        for r in range(self.rows):
            for c in range(self.cols):
                pos = (r,c)
                if pos == self.start:
                    string.append("S")
                elif pos == self.end:
                    string.append("E")
                elif pos in self.space:
                    string.append(" ")
                else:
                    string.append("#")
            string.append("\n")
        return "".join(string)
    
    def build_connections(self):
        connections = set()
        directions = [(0,1),(0,-1),(1,0),(-1,0)] 
        for space in self.space:
            sx,sy = space
            for (dx,dy) in directions:
                neighbour = (sx+dx,sy+dy)
                if neighbour in self.space:
                    connections.add((space,neighbour))
        return list(connections)
    
    def build_path(self):
        def Dijkstra(start,end,graph):
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
                    path = route(node,previous)+[neighbour]
                    cost = self.cost(path)
                    if cost < dist[neighbour]:
                        dist[neighbour] = cost
                        previous[neighbour] = node
                        heapq.heappush(queue,(cost,neighbour))
            return route(end,previous)

        return Dijkstra(self.start,self.end,self._graph)

    def show_route(self,route):
        string = []
        for r in range(self.rows):
            for c in range(self.cols):
                pos = (r,c)
                if pos == self.start:
                    string.append("S")
                elif pos == self.end:
                    string.append("E")
                elif pos in route:
                    string.append("\033[1;33m*\033[0m")
                elif pos in self.space:
                    string.append(" ")
                else:
                    string.append("\033[34m#\033[0m")
            string.append("\n")
        return "".join(string)

    def cost(self,route):
        score = 0
        score += len(route)-1
        facing = complex(0,1)
        for i in range(len(route)-1):
            (x1,y1) = route[i]
            (x2,y2) = route[i+1]
            delta = (x2-x1,y2-y1)
            delta = complex(*delta)
            if delta == 1j*facing or delta == -1j*facing:
                score += 1000
                facing = delta
        return score
            
    def build_maze(self,path):
        file = read_file(path)
        space = set()
        start = None 
        end   = None

        for i,line in enumerate(file):
            line = line.strip()
            for j, char in enumerate(list(line)):
                pos = (i,j)
                if char != "#":
                    space.add(pos)
                    if char == "S":
                        start = pos
                    if char == "E":
                        end = pos
           
        return start,end,space,i+1,j+1

def part1(path):
    course = maze(path)
    min_route = course.build_path()
    print(course.show_route(min_route))
    print(f"Part 1: {course.cost(min_route)}")

def part2(path):
    course = maze(path)
    route = course.build_path()
    print(len(route))

def main(day:int,Test:bool=False):
    path = f"Day{day}/test.txt" if Test else f"Day{day}/input.txt"
    
    part1(path)
    part2(path)

if __name__ == "__main__":
    main(16,True)