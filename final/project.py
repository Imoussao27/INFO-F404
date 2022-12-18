import sys
from math import gcd

from models import *
from Partitioner import *


def readFile(nameFile):
    """
    Read file to create a list with task information
    :param nameFile: name of file
    :return: a list of task
    """
    tasks = []
    period = []
    f = open(nameFile)
    index = 1
    for line in f:
        value = line.strip().split()  # Crée les task
        tasks.append(Task(index, int(value[0]), int(value[1]), int(value[2]), int(value[3])))
        period.append(int(value[3]))
        index += 1
    f.close()

    return tasks, period

def run(algo, res, heuristic, order, cores_number):
    lcm = leastCommonMultiple(res[1])
    partitioner = Partitioner(res[0], heuristic, order, lcm, cores_number)
    switchOrder(partitioner, order)
    switchHeuristic(partitioner, heuristic)

    if partitioner.is_partitioned():
        for core in partitioner.get_cores():
            core.ToPrint()
            core.schedule(algo)
    else:
        print("The partitioning fails")
        exit(1)

def switchHeuristic(partitioner, heuristic):
    return getattr(partitioner, str(heuristic))()

def switchOrder(partitioner, order):
    return getattr(partitioner, str(order))()

def leastCommonMultiple(period):
    """
    Function calculate least common multiple
    :param period: list of period
    :return: int LCM
    """
    lcm = 1
    for elem in period:
        lcm = lcm * elem // gcd(lcm, elem)
    return lcm


if __name__ == '__main__':
    algo = "RM" #TODO: HOW METTRE MAJ
    heuristic = "ff"
    order = "du"
    cores_number = 2
    res = readFile("taskset.txt")  #une liste de task de type task

    run(algo, res, heuristic, order, cores_number)