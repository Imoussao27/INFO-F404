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
    partitioner.heuristicFunction()
    runPartitioner(algo, partitioner)


def runPartitioner(algo, partitioner):
    parti = [processor for processor in partitioner.processors if processor.utilization > 0]
    if partitioner.isPartitioned:
        for core in parti:
            core.ToPrint()
            core.schedule(algo)
    else:
        print("The partitioning fails")
        exit(1)


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
    #./project <tasks_file> -m <#cores> -a edf|rm|dm [-h ff|wf|bf|nf] [-s du|iu]
    heuristic = "ff" #default value
    order = "du" #default value
    #Value Mandatory
    if sys.argv[2] == "-m":
        cores = int(sys.argv[3])
    else:
        exit(5)
    if sys.argv[4] == "-a":
        algo = sys.argv[5]
    else:
        exit(5)

    if sys.argv[6] == "-h":
        heuristic = sys.argv[7]
    if sys.argv[6] == "-s":
        order = sys.argv[7]
    if sys.argv[8] == "-s":
        order = sys.argv[9]

    #Start
    res = readFile(sys.argv[1])
    run(algo, res, heuristic, order, cores)