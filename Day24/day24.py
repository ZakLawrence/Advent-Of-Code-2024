import sys
sys.path.insert(0,"/Users/zlawrence/Documents/LocalWorkArea/Advent-Of-Code-2024")
from shared.common import read_file
from shared.GraphTools import Graph
from graphviz import Digraph, Graph as GVGraph
from collections import defaultdict

function = {
    "AND": (lambda x1,x2: x1 & x2),
    "OR": (lambda x1,x2: x1 | x2),
    "XOR": (lambda x1,x2: x1 ^ x2),
}

class LogicGate:
    def __init__(self, name:str):
        self.name = name
        self.inputs = []

    def add_input(self,gate):
        self.inputs.append(gate)

    def remove_input(self,gate_name):
        self.inputs = [gate for gate in self.inputs if gate.name != gate_name]

    def output(self):
        pass

class InputGate(LogicGate):
    def __init__(self, name, value=False):
        super().__init__(name)
        self.value = value
    
    def set_value(self,value):
        self.value = value
    
    def output(self):
        return self.value

class ANDGate(LogicGate):
    def output(self):
        return all(input_gate.output() for input_gate in self.inputs)

class ORGate(LogicGate):
    def output(self):
        return any(input_gate.output() for input_gate in self.inputs)

class XORGate(LogicGate):
    def output(self):
        return sum(input_gate.output() for input_gate in self.inputs) == 1

class LogicNetwork(Graph):
    def __init__(self,inputs,gates):
        def get_gates(gates):
            connections = []
            logic_gates = {}
            for key, gate in gates.items():
                connections.append((gate["in1"],key,1))
                connections.append((gate["in2"],key,1))
                if gate['function'] == "AND":
                    logic_gates[key] = ANDGate(key) 
                if gate['function'] == "OR":
                    logic_gates[key] = ORGate(key) 
                if gate['function'] == "XOR":
                    logic_gates[key] = XORGate(key) 
            return connections,logic_gates

        self.input_layer = {key:InputGate(key,value) for key,value in inputs.items()}
        self.connections, self.gates = get_gates(gates)
        self.gates = self.gates | self.input_layer
        self.gate_type = {k:v["function"] for k,v in gates.items()} | {k:"" for k,v in inputs.items()}
        for in1,gate,_ in self.connections:
            self.gates[gate].add_input(self.gates[in1])
        super().__init__(self.connections,True)

    def output(self,input_x, input_y):
        inputs = binary_rep(input_x,"x") | binary_rep(input_y,"y")
        for key,value in inputs.items():
            self.gates[key].set_value(value)
        out = {}
        for i in range(46):
            out[f"z{i:02}"] = int(self.gates[f"z{i:02}"].output())
        return out
    
    def visualize(self, output_file="graph", format="png"):
        """Visualize the graph using Graphviz."""
        # Choose the appropriate Graphviz class
        gv_graph = Digraph() if self._directed else GVGraph()

        # Add nodes and edges
        for node1, neighbors in self._graph.items():
            gv_graph.node(node1, label = node1+"\n"+self.gate_type[node1])  # Add the node
            for node2, weight in neighbors.items():
                # Add edges with weights
                gv_graph.edge(node1, node2, label=str(weight))

        # Render the graph
        gv_graph.render(output_file, format=format, cleanup=True)
        print(f"Graph saved to {output_file}.{format}")
    
def binary_rep(num,key):
    bin_rep = bin(num)[2:].zfill(45)
    bin_dict = {}
    for i,bit in enumerate(reversed(bin_rep)):
        bin_dict[f"{key}{i:02}"] = int(bit)
    return bin_dict

def build_output(results):
    outputs = {k:v for k,v in results.items() if k.startswith("z")}
    total = 0 
    for k,v in outputs.items():
        if v:
            total += 2**int(k[1:])
    return total

def build_system(gates,inputs):
    while None in inputs.values():
        for gk,gate in gates.items():
            in1 = inputs[gate["in1"]]
            in2 = inputs[gate["in2"]]
            if in1 != None and in2 != None:
                inputs[gk] = function[gate["function"]](in1,in2)
    return inputs

def parse_input(path):
    inputs = {}
    values = {}
    gates = {}

    def parse_wire(line):
        line = line.split(":")
        inputs[line[0]] = int(line[1].strip()) == 1
        values[line[0]] = int(line[1].strip()) == 1
    
    def pasrse_gate(line):
        line = line.split("->")
        key = line[1].strip()
        gate = line[0].strip()
        in1,func,in2 = gate.split(" ")
        gates[key] = {"function": func,"in1":in1, "in2":in2}
        values[key] = None

    file = read_file(path)
    for line in file:
        line = line.strip()
        if line == "":
            continue
        if ":" in line:
            parse_wire(line)
        else:
            pasrse_gate(line)
    return values,inputs,gates

def part1(path):
    values,_,gates = parse_input(path)
    results = build_system(gates,values)
    output = build_output(results)
    print(f"Part 1: {output}")

def compare_dics(dict1,dict2):
    differences = []
    for key in dict1:
        if dict1[key] != dict2[key]:
            differences.append((key,dict1[key],dict2[key]))
    return differences

def part2(path):
    values,inputs,gates = parse_input(path)
    network = LogicNetwork(inputs,gates)

    one = 1
    for i in range(45):
        x = one <<i
        y = one <<i
        z = x+y 
        sum_z = binary_rep(z,"z")
        result = network.output(x,y)
        print(i,compare_dics(sum_z,result))



    network.visualize(format="pdf")

def main(day:int,Test:bool=False):
    path = f"Day{day}/test.txt" if Test else f"Day{day}/input.txt" 
    part1(path)
    part2(path)

if __name__ == "__main__":
    main(24)