import os 
import sys
sys.path.insert(0,"/Users/zlawrence/Documents/LocalWorkArea/Advent-Of-Code-2024")
from shared.common import read_file

def make_reports(lines):
    reports = []
    for line in lines:
        line = line.strip()
        report = [int(x) for x in line.split(" ")]
        reports.append(report)
    return reports

def safe(diffs):
    if 0 in diffs:
        return False
    if max([abs(x) for x in diffs]) > 3:
        return False
    if all(x > 0 for x in diffs) or all(x < 0 for x in diffs):
        return True
    return False

def remove(list,i):
    copy = list.copy()
    copy.pop(i)
    return copy

def safe_damped(diffs):
    tests = []
    for i in range(0,len(diffs)):
        tests.append(safe(remove(diffs,i)))
    print(tests)

def analyse_reports_damped(reports):
    results = []
    for report in reports:
        tests = []
        for i in range(0,len(report)):
            popped_list = remove(report,i)
            diffs = [popped_list[j+1] - popped_list[j] for j in range(len(popped_list)-1)]
            tests.append(safe(diffs))
        results.append(any(tests))
    return results

def analyse_reports(reports):
    results = []
    for report in reports:
        diffs = [report[i+1] - report[i] for i in range(len(report)-1)]
        results.append(safe(diffs))
    return results

def main(Test:bool=False):
    path = "Day2/test.txt" if Test else "Day2/input.txt"
    file = read_file(path)
    reports = make_reports(file)
    results = analyse_reports(reports)
    print("Part 1: ", sum(results))
    damped = analyse_reports_damped(reports)
    print("Part 2: ", sum(damped))


if __name__ == "__main__":
    main()