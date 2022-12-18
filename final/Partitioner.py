from Scheduler import Scheduler
from algos import RM, EDF, DM

class Processor:
    def __init__(self, id):
        self.id = id
        self.tasks = []
        self.utilization = 0
        self.scheduler = Scheduler(self.tasks)

    def ToPrint(self):
        res = ""
        for task in self.tasks:
            res += "T{}, ".format(task.id)
        print("Processor {} : ".format(self.id) + res[:-1])

    def addTask(self, task):
        self.tasks.append(task)
        self.utilization += task.utilization

    def deleteTask(self):
        task = self.tasks.pop()
        self.utilization -= task.utilization

    def isScheduling(self, lcm):
        return self.scheduler.is_scheduling(lcm)

    def schedule(self, algo):
        if algo == "rm":
            functionNameAlgo = RM(self.tasks)
        elif algo == "dm":
            functionNameAlgo = DM(self.tasks)
        else:
            functionNameAlgo = EDF(self.tasks)
        feasibility, allTasks = self.scheduler.runAlgo(functionNameAlgo)
        self.scheduler.algo.toPrint(feasibility, allTasks)


class Partitioner:
    def __init__(self, tasks, heuristic, sort, lcm, processors_number):
        self.heuristic = heuristic #ff wf bf nf
        self.sort = sort  #du iu
        self.lcm = lcm
        self.tasks = tasks #list of task
        self.processors = [Processor(i + 1) for i in range(processors_number)]
        self.sizeprocessor = len(self.processors)
        self.lastProcessor = 0
        self.isPartitioned = True

    def heuristicFunction(self):
        processor = 0
        if self.heuristic == "nf":
            processor = self.lastProcessor
        # First Fit
        for task in self.tasks:
            if not self.isPlaced(task, processor):
                self.isPartitioned = False
            # Worst fit
            if self.heuristic == "wf":
                self.processors.sort(key=lambda partition: partition.utilization)

            # Best fit
            if self.heuristic == "bf":
                self.processors.sort(key=lambda partition: partition.utilization, reverse=True)

        # utilisation

        if self.sort == "du":
            self.tasks.sort(key=lambda task: task.utilization, reverse=True)
        else:  # iu
            self.tasks.sort(key=lambda task: task.utilization)

    def isPlaced(self, task, current):
        copy = current
        while copy < self.sizeprocessor:
            self.lastProcessor = copy
            self.processors[copy].addTask(task) #add task
            res = self.processors[copy].isScheduling(self.lcm) #verify scheduling
            task.reset()
            if res:
                return True
            else:
                self.processors[copy].deleteTask()
                copy += 1
        return False

