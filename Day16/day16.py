import sys
sys.path.insert(0,"/Users/zlawrence/Documents/LocalWorkArea/Advent-Of-Code-2024")
from shared.common import read_file
import heapq

class maze:
    def __init__(self,path):
        self.start, self.end, self.space,self.rows,self.cols = self.build_maze(path)

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

    def build_paths(self):
        directions = [(0,1),(0,-1),(1,0),(-1,0)] 
        def step(position,route,cost,min_cost):
            if position == self.end:
                return [route], cost
            
            if cost > min_cost[0]:
                return [], min_cost[0]

            pr,pc = position
            all_routes = []
            for (dr,dc) in directions:
                newpos = (pr+dr,pc+dc)
                if newpos in self.space and newpos not in route:
                    new_route = route+[position]
                    new_cost = self.cost(new_route)
                    new_routes, updated_min_cost = step(newpos,new_route,new_cost,min_cost)
                    min_cost[0] = min(min_cost[0],updated_min_cost)

                    all_routes.extend(new_routes)
            return all_routes,min_cost[0]
        
        def heuristic(a,b):
            cost = abs(a[0]-b[0]) + abs(a[1]-b[1])
            if abs(a[0]-b[0]) != 0 and abs(a[1]-b[1]) !=0:
                cost += 1000
            return cost
        
        def a_star_search(start,end,space):
            open_set = []
            heapq.heappush(open_set, (0, start))

            g_cost = {start: 0}
            came_from = {}

            while open_set:
                _, current = heapq.heappop(open_set)
                if current == end:
                    path = []
                    while current in came_from:
                        path.append(current)
                        current = came_from[current]
                    path.append(start)
                    return path[::-1]

                pr, pc = current
                for dr,dc in directions:
                    neighbor = (pr + dr, pc + dc)

                    if neighbor not in space:
                        continue

                    tentative_g = g_cost[current] + 1 
                    if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                        g_cost[neighbor] = tentative_g
                        f_cost = tentative_g + heuristic(neighbor, end)
                        heapq.heappush(open_set, (f_cost, neighbor))
                        came_from[neighbor] = current
            return None

        def step_iterative(start, end, space):
            stack = [(start, [start], 0)]  # (current position, route, cost)
            minimal_route = a_star_search(start,end,space)
            min_cost = self.cost(minimal_route)
            all_routes = []

            while stack:
                position, route, cost = stack.pop()

                # If we've reached the endpoint
                if position == end:
                    if cost < min_cost:
                        min_cost = cost  # Update the minimum cost
                    all_routes.append(route)
                    continue

                # Prune branches that exceed the minimum cost
                if cost > min_cost:
                    continue

                pr, pc = position
                for (dr, dc) in directions:
                    newpos = (pr + dr, pc + dc)
                    if newpos not in space:
                        continue

                    if newpos in space and newpos not in route:
                        new_cost = self.cost(route + [newpos])
                        stack.append((newpos, route + [newpos], new_cost))

            return all_routes, min_cost

        #routes,_ = step(self.start,[],0,min_cost)
        routes,_ = step_iterative(self.start,self.end,self.space)

        return routes

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

    def minimum_route(self,routes):
        cost = 1e50
        min_route = None 
        for route in routes:
            route_cost = self.cost(route)
            print(route_cost)
            print(self.show_route(route))
            if route_cost < cost:
                cost = route_cost
        return cost

    def cost(self,route):
        score = 0
        score += len(route)
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


def main(day:int,Test:bool=False):
    path = f"Day{day}/test2.txt" if Test else f"Day{day}/input.txt"

    course = maze(path)
    print(course)
    print(course.start)
    routes = course.build_paths()
    print(len(routes))
    Cost = course.minimum_route(routes)
    print(f"Part 1: {Cost}")


if __name__ == "__main__":
    main(16)