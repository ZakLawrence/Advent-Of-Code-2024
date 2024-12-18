import sys
sys.path.insert(0,"/Users/zlawrence/Documents/LocalWorkArea/Advent-Of-Code-2024")
from shared.common import read_file

class Compute:
    def __init__(self):
        self.pointer_position = 0
        self.next_step = True
        self.to_print = []

    def step(self):
        self.pointer_position += 2

    def set_registerA(self,value):
        self.registerA = value

    def input_program(self,path):
        file = read_file(path)
        lines = file.readlines()
        lines = [line.strip() for line in lines if line.strip()]
        self.registerA = int(lines[0].split(':')[1])
        self.registerB = int(lines[1].split(':')[1])
        self.registerC = int(lines[2].split(':')[1])
        self.program = list(map(int,lines[3].split(':')[1].split(',')))

    def combo(self,in1):
        if in1 <= 3:
            return in1
        elif in1 == 4:
            return self.registerA
        elif in1 == 5:
            return self.registerB
        elif in1 == 6:
            return self.registerC
        else:
            raise RuntimeError(f"Got unexpected combo {in1}!")
        
    def adv(self,in1):
        numerator = self.registerA
        denominator = 2**self.combo(in1)
        self.registerA = int(numerator/denominator)
    
    def bxl(self,in1):
        res = self.registerB ^ in1
        self.registerB = res
    
    def bst(self,in1):
        res = self.combo(in1)%8
        self.registerB = res
    
    def jnz(self,in1):
        regA = self.registerA
        if regA !=0:
            self.pointer_position = in1
            self.next_step = False
    
    def bxc(self,in1):
        res = self.registerB ^ self.registerC
        self.registerB = res
    
    def out(self,in1):
        res = self.combo(in1)%8
        self.to_print.append(str(res))
    
    def bdv(self,in1):
        numerator = self.registerA
        denominator = 2**self.combo(in1)
        self.registerB = int(numerator/denominator)
    
    def cdv(self,in1):
        numerator = self.registerA
        denominator = 2**self.combo(in1)
        self.registerC = int(numerator/denominator)
        
    def get_cmd(self,cmd):
        if cmd == 0:
            return self.adv
        elif cmd == 1: 
            return self.bxl
        elif cmd == 2: 
            return self.bst
        elif cmd == 3:
            return self.jnz
        elif cmd == 4:
            return self.bxc
        elif cmd == 5: 
            return self.out
        elif cmd == 6:
            return self.bdv
        elif cmd == 7: 
            return self.cdv
        else:
            raise RuntimeError(f"Invalid command {cmd}")
        

    def read_program(self,pointer_position,program):
        if pointer_position < (len(program)-1):
            return program[pointer_position],program[pointer_position+1]

    def run_program(self):
        while self.pointer_position < (len(self.program) - 1):
            self.next_step = True
            cmd,opr = self.read_program(self.pointer_position,self.program)
            func = self.get_cmd(cmd)
            func(opr)
            if self.next_step:
                self.step()
        print(",".join(self.to_print))            
        return self.to_print

def func_out(A):
    B = A%8
    B = B^1
    C = int(A/(2**B))
    A = int(A/(2**3))
    B = B^4
    B = B^C
    return B%8

def func(A):
    string = []
    while A != 0:
        B = A%8
        B = B^1
        C = int(A/(2**B))
        A = int(A/(2**3))
        B = B^4
        B = B^C
        string.append(str(B%8))
    #print(','.join(string))
    return string

def search(to_find):
    possibe = {0}
    for num in reversed(to_find):
        test = set()
        for current in possibe:
            for i in range(8):
                new = (current << 3) + i
                if func_out(new) == num:
                    test.add(new)
        possibe = test
    return min(possibe)

def part1(path):
    program = Compute()
    program.input_program(path)
    print("Part 1:")
    program.run_program()

def part2(path):
    program = Compute()
    program.input_program(path)
    to_find = program.program
    print(f"Part 2: {search(to_find)}")

def main(day:int,Test:bool=False):
    path = f"Day{day}/test.txt" if Test else f"Day{day}/input.txt"
    part1(path)
    part2(path)

if __name__ == "__main__":
    main(17)

