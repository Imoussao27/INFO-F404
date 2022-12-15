import sys
import getopt
from Task import *


class Parser:
    def __init__(self, filename="taskset.txt", heuristic="ff", sort="du", limit=400, cores_number=2):
        """
        An parser class that allows you to obtain the tasks from the task file and the options chosen to run the
        simulator.
        """
        self.filename = filename
        self.heuristic = heuristic
        self.sort = sort
        self.limit = limit
        self.cores_number = cores_number

    def get_options(self):
        """
        Get the options to be used for the simulation

        :return: the options tuple
        """
        return self.heuristic, self.sort, self.limit, self.cores_number

    def get_tasks(self):
        """
        Get the tasks that have to be scheduled from the task set file

        :return: the list of the tasks
        """
        tasks = []
        f = open(self.filename)
        i = 0
        for line in f:
            value = line.strip().split() #Crée les task
            tasks.append(Task(i, int(value[0]), int(value[1]), int(value[2]), int(value[3])))
            i += 1
        f.close()

        return tasks