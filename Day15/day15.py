import sys
sys.path.insert(0,"/Users/zlawrence/Documents/LocalWorkArea/Advent-Of-Code-2024")
from shared.common import read_file
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

class Object:
    def __init__(self,position,movable=True):
        self.position = position
        self.movable = movable

    def get_position(self):
        return self.position

    def is_movable(self):
        return self.movable    
    
    def update_position(self,new_position):
        if self.movable:
            self.position = new_position

    def change_position(self,new_position):
        self.position = new_position
    
    def value(self):
        py,px = self.position
        return 100*py + px

    def __eq__(self, value):
        return self.position == value

class Object_Wide(Object):
    def __init__(self, position, movable=True):
        super().__init__(position,movable)
        self.positions = (position, (position[0],position[1]+1))
    
    def get_position(self):
        return self.positions
    
    def update_position(self, new_positions):
        if self.movable:
            self.positions = new_positions
    
    def value(self):
        (py,px),_ = self.positions
        return 100*py+px
    
    def __eq__(self, value):
        return value == self.positions[0] or value == self.positions[1]

class Wearhouse:
    def __init__(self,file_path):
        def parse_inputs(path):
            
            def build_grid(grid_lines):
                walls = []
                boxes = []
                robot = None
                for i,line in enumerate(grid_lines):
                    for j,char in enumerate(list(line)):
                        if char == ".":
                            continue
                        elif char == "#":
                            walls.append(Object((i,j),False))
                        elif char == "O":
                            boxes.append(Object((i,j)))
                        elif char == "@":
                            robot = Object((i,j))
                return walls,boxes,robot
            
            def parse_moves(move_lines):
                moves = []
                for line in move_lines:
                    for char in list(line):
                        if char == "^":
                            moves.append((-1,0))
                        elif char == ">":
                            moves.append((0,1))
                        elif char == "v":
                            moves.append((1,0))
                        elif char == "<":
                            moves.append((0,-1))
                return moves

            
            file = read_file(path)
            grid = []
            moves = []
            end_grid = False
            for line in file: 
                line = line.strip()
                if line == "":
                    end_grid = True
                    continue
                if end_grid:
                    moves.append(line)
                else:
                    grid.append(line)
            Nrows = len(grid)
            Ncols = len(grid[0])
            walls,boxes,robot = build_grid(grid)
            moves = parse_moves(moves)

            return Nrows,Ncols,walls,boxes,robot,moves

        self.Nrows,self.Ncols,self.walls,self.boxes,self.robot,self.moves = parse_inputs(file_path)        

    def set_walls(self,walls):
        self.walls = walls

    def set_boxes(self,boxes):
        self.boxes = boxes

    def scale_grid(self):
        walls = []
        boxes = []
        for wall in self.walls:
            wall_pos = wall.get_position()
            wall.change_position((wall_pos[0],wall_pos[1]*2))
            walls.append(wall)
            walls.append(Object(wall_pos))
        self.set_walls(walls)
        for box in self.boxes:
            box_pos = box.get_position()
            wide_pos = (box_pos[0],box_pos[1]+1)
            boxes.append((box_pos,wide_pos))
        self.set_boxes(boxes)

    def is_wall(self,pos):
        return pos in [wall.get_position() for wall in self.walls]
    
    def is_box(self,pos):
        return pos in [box.get_position() for box in self.boxes]
    
    def move_box_chain(self,pos,dx,dy):
        chain = []
        current_pos = pos

        while self.is_box(current_pos):
            chain.append(current_pos)
            current_pos = (current_pos[0]+dx,current_pos[1]+dy)
        
        if self.is_wall(current_pos):
            return False
        
        for box_pos in reversed(chain):
            for box in self.boxes:
                if box.get_position() == box_pos:
                    box.update_position((box_pos[0]+dx,box_pos[1]+dy))
        
        return True

    def run_movements(self):
        for (dx,dy) in self.moves:
            bx,by = self.robot.get_position()
            nx,ny = bx+dx,by+dy
            if (nx,ny) in self.walls:
                continue
            if (nx,ny) in self.boxes:
                if not self.move_box_chain((nx,ny),dx,dy):
                    continue
            self.robot.update_position((nx,ny))

    def value(self):
        return sum(box.value() for box in self.boxes)

    def __str__(self):
        string = []
        for i in range(self.Nrows):
            for j in range(self.Ncols):
                pos = (i,j)
                if self.is_wall(pos):
                    string.append("\033[34m#\033[0m")
                elif self.is_box(pos):
                    string.append("\033[32mO\033[0m")
                elif pos == self.robot:
                    string.append("\033[1;33m@\033[0m")
                else:
                    string.append(" ")
            string.append("\n")
        return "".join(string)



class WearhouseAnimation(Wearhouse):  # Extend your existing Wearhouse class
    def __init__(self, file_path):
        super().__init__(file_path)
        self.frames = []  # To store the state of the warehouse at each step

    def save_frame(self):
        """Save the current grid as a frame."""
        grid = [[" " for _ in range(self.Ncols)] for _ in range(self.Nrows)]
        # Add walls
        for wall in self.walls:
            wx, wy = wall.get_position()
            grid[wx][wy] = "#"

        # Add boxes
        for box in self.boxes:
            bx, by = box.get_position()
            grid[bx][by] = "O"

        # Add robot
        rx, ry = self.robot.get_position()
        grid[rx][ry] = "@"

        # Convert grid to a NumPy array for visualization
        self.frames.append(np.array(grid))

    def run_movements_with_animation(self):
        """Run movements and save frames for animation."""
        self.save_frame()  # Initial state
        for (dx, dy) in self.moves:
            # Current robot position
            bx, by = self.robot.get_position()

            # Desired new position
            nx, ny = bx + dx, by + dy

            if (nx,ny) in self.walls:
                continue
            if (nx,ny) in self.boxes:
                if not self.move_box_chain((nx,ny),dx,dy):
                    continue
    
            # Move the robot if the path is clear or the stack moved successfully
            self.robot.update_position((nx, ny))

            self.save_frame()  # Save the frame after each movement

    def animate(self):
        """Create and display the animation."""
        # Convert frames to numeric grid for visualization
        def grid_to_numeric(frame):
            # Map characters to integers for display
            char_map = {" ": 0, "#": 1, "O": 2, "@": 3}
            numeric_grid = [[char_map[char] for char in row] for row in frame]
            return np.array(numeric_grid)

        numeric_frames = [grid_to_numeric(frame) for frame in self.frames]

        fig, ax = plt.subplots(figsize=(6, 6))
        img = ax.imshow(numeric_frames[0], cmap="viridis", interpolation="nearest")

        def update(frame_idx):
            """Update the grid for each frame."""
            img.set_data(numeric_frames[frame_idx])
            return img,

        ani = FuncAnimation(fig, update, frames=len(numeric_frames), blit=True, interval=10)

        # Optionally, save the animation
        ani.save("robot_movement.mp4", writer="ffmpeg")



    
def part1(path):
    wearhouse = Wearhouse(path)
    print(wearhouse)
    wearhouse.run_movements()
    print(wearhouse)
    print(f"Part 1: {wearhouse.value()}")


def main(day:int,Test:bool=False):
    path = f"Day{day}/test.txt" if Test else f"Day{day}/input.txt"
    part1(path)
    #if Test:
    #    wearhouse = WearhouseAnimation(path)
    #    wearhouse.run_movements_with_animation()
    #    wearhouse.animate()

if __name__ == "__main__":
    main(15,True)