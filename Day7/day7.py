import sys
sys.path.insert(0,"/Users/zlawrence/Documents/LocalWorkArea/Advent-Of-Code-2024")
from shared.common import read_file
from tqdm.auto import tqdm


def can_form_result_concatination(result,current,numbers):
    if current > result:
        return False
    elif len(numbers) == 0:
        return result == current
    else:
        head, *tail = numbers
        mul_value = current * head
        add_value = current + head
        merge_value = int(''.join([str(current),str(head)]))
        return can_form_result_concatination(result,mul_value,tail) or can_form_result_concatination(result,add_value,tail) or can_form_result_concatination(result,merge_value,tail)

def can_form_result(result,current,numbers):
    if current > result: 
        return False
    elif len(numbers) == 0: 
        return result == current
    else:
        head, *tail = numbers
        mul_value = current * head
        add_value = current + head
        return can_form_result(result,mul_value,tail) or can_form_result(result,add_value,tail)

def validate_sums_extended(sums):
    for eq in tqdm(sums):
        head, *tail = eq["inputs"]
        res = can_form_result(eq["total"],head,tail)
        eq["valid"] = res if res else can_form_result_concatination(eq["total"],head,tail)
    return sum([eq["total"] for eq in sums if eq["valid"]])

def validate_sums(sums):
    for eq in tqdm(sums):
        head, *tail = eq["inputs"]
        eq["valid"] = can_form_result(eq["total"],head,tail)
    return sum([eq["total"] for eq in sums if eq["valid"]])

def get_sums(lines):
    sums = []
    for index,line in enumerate(lines):
       line = line.strip()
       total,inputs = line.split(":") 
       inputs = [int(x) for x in inputs.split(" ") if x]
       sums.append({"total":int(total),"inputs":inputs,"valid":False,"Solution":None})
    return sums

def part2(sums):
    print(f"Part 2: {validate_sums_extended(sums)}")

def part1(path):
    file = read_file(path)
    sums = get_sums(file)
    print(f"Part 1: {validate_sums(sums)}")
    return sums



def main(Test:bool=False):
    path = "Day7/test.txt" if Test else "Day7/input.txt"
    sums = part1(path)
    part2(sums)

if __name__ == "__main__":
    main()