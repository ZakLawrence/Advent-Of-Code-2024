import sys
sys.path.insert(0,"/Users/zlawrence/Documents/LocalWorkArea/Advent-Of-Code-2024")
from shared.common import read_file
from collections import defaultdict
import heapq
from itertools import combinations

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

    def find_cliques(self,n):
        if n <=1:
            raise ValueError(f"Must search for groups of size greater than 1!")
        nodes = list(self._graph.keys())
        cliques = []
        for subset in combinations(nodes,n):
            if self.is_clique(subset):
                cliques.append(set(subset))
        return cliques
    
    def is_clique(self,subset):
        for i,node1 in enumerate(subset):
            for node2 in subset[i+1:]:
                if node2 not in self._graph[node1]:
                    return False
        return True
    
    def find_largest_clique(self):
        def Bron_Kerbosch(R,P,X):
            if not P and not X:
                maximal_cliques.append(R)
                return
            for v in list(P):
                Bron_Kerbosch(R|{v},P & self._graph[v].keys(), X & self._graph[v].keys())
                P.remove(v)
                X.add(v)
        maximal_cliques = []
        Bron_Kerbosch(set(),set(self._graph.keys()),set())
        largest_clique = max(maximal_cliques,key=len)
        return largest_clique

    def __str__(self):
        """Pretty-print the graph structure."""
        return str(dict(self._graph))

def parse_graph(path):
    file = read_file(path)
    connections = []
    for line in file:
        line = line.strip()
        nodes = line.split("-")
        connections.append( (nodes[0],nodes[1],1))
    return Graph(connections)

def part1(path):
    lan_party = parse_graph(path)
    cliques = lan_party.find_cliques(3)
    tsets = [clique for clique in cliques if any(elem.startswith('t') for elem in clique) ]
    print(f"Part 1: {len(tsets)}")

def part2(path):
    lan_party = parse_graph(path)
    maximum_clique = lan_party.find_largest_clique()
    maximum_clique = sorted(list(maximum_clique)) 
    print(f"Part 2: {",".join(maximum_clique)}")

def main(day:int,Test:bool=False):
    path = f"Day{day}/test.txt" if Test else f"Day{day}/input.txt" 
    part1(path)
    part2(path)

if __name__ == "__main__":
    main(23)