import sys
sys.path.insert(0,"/Users/zlawrence/Documents/LocalWorkArea/Advent-Of-Code-2024")
from shared.common import read_file


def add_antenna(antennas,key,pos):
    if key in antennas:
        antennas[key].append(pos)
    else: 
        antennas[key] = [pos]
    return antennas

def find_antennas(path):
    antennas = {}
    file = read_file(path)
    Nrows, Ncols = 0,0
    for i,line in enumerate(file):
        line = line.strip()
        row = list(line)
        Ncols = len(row)
        Nrows = i
        for j in range(len(row)):
            if row[j] != ".":
                antennas = add_antenna(antennas,row[j],(i,j))
    return antennas, Nrows+1, Ncols        

def calculate_antinodes(pos1,pos2):
    dx = pos1[0]-pos2[0]
    dy = pos1[1]-pos2[1]
    a1 = (pos1[0]+dx,pos1[1]+dy)
    a2 = (pos2[0]-dx,pos2[1]-dy)
    return a1,a2

def calculate_antinodes_resonance(pos1,pos2,rows,cols):
    antinodes = []
    dx = pos1[0]-pos2[0]
    dy = pos1[1]-pos2[1]
    i = 0
    condition = (lambda x,y: 0 <= x < y) 
    while condition(pos1[0]+i*dx,rows) and condition(pos1[1]+i*dy,cols):
        antinodes.append((pos1[0]+i*dx,pos1[1]+i*dy))
        i+=1
    i=0
    while condition(pos2[0]-i*dx,rows) and condition(pos2[1]-i*dy,cols):
        antinodes.append((pos2[0]-i*dx,pos2[1]-i*dy))
        i+=1
    return antinodes

def find_antinodes_res(antennas,rows,cols):
    total_antinodes = []
    for key, positions in antennas.items():
        pairs = [(a,b) for idx, a in enumerate(positions) for b in positions[idx+1:]]
        for pos1,pos2 in pairs:
            antinodes = calculate_antinodes_resonance(pos1,pos2,rows,cols)
            total_antinodes = total_antinodes + antinodes
    print(len(set(total_antinodes)))

def find_antinodes(antennas,rows,cols):
    antinodes = []
    for key, positions in antennas.items():
        pairs = [(a,b) for idx, a in enumerate(positions) for b in positions[idx+1:]]
        for pos1,pos2 in pairs:
            a1,a2 = calculate_antinodes(pos1,pos2)
            if 0 <= a1[0] < rows and 0 <= a1[1] < cols:
                antinodes.append(a1)
        
            if 0 <= a2[0] < rows and 0 <= a2[1] < cols:
                antinodes.append(a2)
    print(len(set(antinodes)))




def main(Test:bool=False):
    path = "Day8/test.txt" if Test else "Day8/input.txt"
    antennas, Rows, Cols = find_antennas(path)

    find_antinodes(antennas,Rows,Cols)
    find_antinodes_res(antennas,Rows,Cols)

if __name__ == "__main__":
    main()