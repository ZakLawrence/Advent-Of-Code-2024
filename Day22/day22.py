import sys
sys.path.insert(0,"/Users/zlawrence/Documents/LocalWorkArea/Advent-Of-Code-2024")
from shared.common import read_file
from math import floor

cache = {}
stocks = {}
sequences = {}

def analyse_sequence(sequence):
    deltas = [b - a for a,b in zip(sequence,sequence[1:])]
    seqs = [(deltas[i:i+4],sequence[i+4]) for i in range(len(deltas)-3)]
    used_seq = set()
    for seq,value in seqs:
        seq = tuple(seq)
        if seq not in used_seq:
            if seq in sequences:
                sequences[seq] += value
            else:
                sequences[seq] = value
            used_seq.add(seq)
    return seqs

def next_secret_number(secret_number):
    if secret_number in cache:
        return cache[secret_number]

    result = secret_number
    result = (result << 6) ^ result
    result %= 2**24
    result = (result >> 5) ^ result
    result %= 2**24
    result = (result << 11) ^ result
    result %= 2**24

    cache[secret_number] = result
    return result

def iterate_secret_numbers(start,iters):
    prices = []
    secret_number = start
    for _ in range(iters):
        result = next_secret_number(secret_number)
        secret_number = result
        prices.append(secret_number%10)
    stocks[start] = prices
    return secret_number

def get_secret_numbers(path):
    file = read_file(path)
    secret_numbers = []
    for line in file:
        secret_numbers.append(int(line.strip()))
    return secret_numbers

def part1(path):
    secret_numbers = get_secret_numbers(path)
    total = 0
    for secret_number in secret_numbers:
        result = iterate_secret_numbers(secret_number,2000)
        total += result
    print(f"Part 1: {total}")

def part2():
    for key,sequence in stocks.items():
        analyse_sequence(sequence)
    print(f"Part 2: {sequences[max(sequences,key=sequences.get)],max(sequences,key=sequences.get)}")



def main(day:int,Test:bool=False):
    path = f"Day{day}/test.txt" if Test else f"Day{day}/input.txt" 
    part1(path)
    part2()

if __name__ == "__main__":
    main(22)