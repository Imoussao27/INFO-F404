import sys
from Task import *
from Partitioner import *


def readFile(nameFile):
    """
    Read file to create a list with task information
    :param nameFile: name of file
    :return: a list of task
    """
    tasks = []
    f = open(nameFile)
    index = 0
    for line in f:
        value = line.strip().split()  # Crée les task
        tasks.append(Task(index, int(value[0]), int(value[1]), int(value[2]), int(value[3])))
        index += 1
    f.close()

    return tasks

def run(tasks, heuristic, sort, limit, cores_number):
    partitioner = Partitioner(tasks, heuristic, sort, limit, cores_number)  # genre limit = 400
    switchHeuristic(partitioner, heuristic)

    if partitioner.is_partitioned():
        for core in partitioner.get_cores():
            print(core)
            core.schedule(limit)
    else:
        print("Cannot be partitioned")

def switchHeuristic(partitioner, heuristic):
    return getattr(partitioner, str(heuristic) + '_fit')()


if __name__ == '__main__':
    heuristic = "ff"
    sort = "du"
    limit = 400
    cores_number = 2
    tasks = readFile("taskset.txt")  #une liste de task de type task

    run(tasks, heuristic, sort, limit, cores_number)