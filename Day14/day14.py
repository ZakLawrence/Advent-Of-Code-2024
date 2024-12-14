import sys
sys.path.insert(0,"/Users/zlawrence/Documents/LocalWorkArea/Advent-Of-Code-2024")
from shared.common import read_file
import numpy as np
import matplotlib.pyplot as plt

class Bot: 
    def __init__(self,position,veleocity,boundary):
        self.position = position
        self.velocity = veleocity
        self.boundary = boundary

    def get_position(self):
        return self.position
    

    def move(self):
        def wrap(coord,limit):
            if 0 <= coord < limit:
                return coord
            else:
                if coord < 0:
                    return limit - abs(coord)
                if coord >= limit:
                    return coord - limit


        px,py = self.position
        vx,vy = self.velocity
        C,R = self.boundary
        nx,ny = wrap(px+vx,C),wrap(py+vy,R)
        #print((px,py),(vx,vy),(nx,ny))
        self.position = (nx,ny)


class Room:
    def __init__(self,NRows,NCols,input_path):
        self.Nrows = NRows
        self.Ncols = NCols
        self.bots = self.parse_inputs(input_path)

    def bot_positions(self):
        return [bot.get_position() for bot in self.bots]

    def parse_inputs(self,path):

        def coordinates(part):
            coord = part.split("=")[1]
            cx,cy = map(int,coord.split(","))
            return(cx,cy)

        bots = []
        file = read_file(path)
        for line in file:
            line = line.strip()
            pos, vel = line.split(" ")
            pos = coordinates(pos)
            vel = coordinates(vel)
            bots.append(Bot(pos,vel,(self.Ncols,self.Nrows)))
        return bots
    
    def __str__(self):
        string = []
        bot_positions = self.bot_positions()
        for i in range(self.Nrows):
            for j in range(self.Ncols):
                if (j,i) in bot_positions:
                    Nbots = len([bot for bot in bot_positions if bot == (j,i)])
                    string.append(str(Nbots))
                else:
                    string.append(".")
            string.append("\n")
        return "".join(string)
    
    def move(self,steps):
        variances = []
        for i in range(steps):
            for bot in self.bots:
                bot.move()
            vx,vy = self.variance()
            variances.append(self.variance())
            if vx < 700 and vy < 700: # Trust me bro these numbers work 
                print(f"Part 2: {i+1}")
                print(self)
        return variances
    
    def saefty_factor(self):
       qc,qr =  (self.Ncols-1)/2 , (self.Nrows-1)/2
       bot_position = self.bot_positions()
       q1 = [bot for bot in bot_position if bot[0]<qc and bot[1]<qr]
       q2 = [bot for bot in bot_position if bot[0]>qc and bot[1]<qr]
       q3 = [bot for bot in bot_position if bot[0]<qc and bot[1]>qr]
       q4 = [bot for bot in bot_position if bot[0]>qc and bot[1]>qr]
       return len(q1)*len(q2)*len(q3)*len(q4)
    
    def variance(self):
        bot_positions = self.bot_positions()
        x = [bot[0] for bot in bot_positions]
        y = [bot[1] for bot in bot_positions]
        varx, vary = np.var(x),np.var(y)
        return varx,vary 

def plot(var,name):
    plt.scatter(range(len(var)),var)
    plt.savefig(name)


def part1(path,Test):
    width,height = 11 if Test else 101, 7 if Test else 103
    room = Room(height,width,path)
    #print(room)
    room.move(100)
    #print(room)
    print(f"Part 1: {room.saefty_factor()}")

def part2(path,Test):
    width,height = 11 if Test else 101, 7 if Test else 103
    room = Room(height,width,path)
    variances = room.move(10000)
    vx = [v[0] for v in variances]
    vy = [v[1] for v in variances]
    plot(vx,"Day14/varx.png")
    plot(vy,"Day14/vary.png")

    


def main(day:int,Test:bool=False):
    path = f"Day{day}/test.txt" if Test else f"Day{day}/input.txt"
    part1(path,Test)
    part2(path,Test)
    

if __name__ == "__main__":
    main(14)
