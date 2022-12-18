from Scheduler import Scheduler
from algos import RM, EDF, DM


class Processor:
    def __init__(self, id):
        """
        A core class containing a tasks set

        :param id: the core identifier and it is unique
        """
        self.id = id
        self.tasks = []
        self.utilization = 0
        self.scheduler = Scheduler(self.tasks) #TODO: call the good algo

    def ToPrint(self):
        res = ""
        for task in self.tasks:
            res += "T{}, ".format(task.id)
        print("Processor {} : ".format(self.id) + res[:-1])

    def add_task(self, task):
        self.tasks.append(task)
        self.utilization += task.utilization

    def remove_task(self):
        task = self.tasks.pop()
        self.utilization -= task.utilization

    def get_utilization(self):
        return self.utilization

    def get_tasks(self):
        return self.tasks

    def is_scheduling(self, limit):
        return self.scheduler.is_scheduling(limit)

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
    def __init__(self, tasks, heuristic, sort, lcm, cores_number):
        self.heuristic = heuristic #ff wf bf nf
        self.sort = sort  #du iu
        self.lcm = lcm
        self.tasks = tasks #list of task
        self.cores = [Processor(i + 1) for i in range(cores_number)]
        self.sizeCore = len(self.cores)
        self.last_core_used = 0
        self.can_be_partitioned = True

    def is_partitioned(self):
        return self.can_be_partitioned

    def get_cores(self):
        return [core for core in self.cores if core.get_utilization() > 0]

    def can_be_placed(self, task, current):
        copy_current = current
        while copy_current < self.sizeCore:
            self.last_core_used = copy_current
            self.cores[copy_current].add_task(task) #add task
            res = self.cores[copy_current].is_scheduling(self.lcm) #verify scheduling
            task.reset()
            if not res:
                self.cores[copy_current].remove_task()
                copy_current += 1
            else:
                return True
        return False

    def ff(self):
        """
        First fit
        """
        for task in self.tasks:
            if not self.can_be_placed(task, 0):
                self.can_be_partitioned = False

    def wf(self):
        """
        Worst fit
        """
        for task in self.tasks:
            if not self.can_be_placed(task, 0):
                self.can_be_partitioned = False
            self.cores.sort(key=lambda partition: partition.utilization)

    def bf(self):
        """
        Best fit
        """
        for task in self.tasks:
            if not self.can_be_placed(task, 0):
                self.can_be_partitioned = False
            self.cores.sort(key=lambda partition: partition.utilization, reverse=True)

    def nf(self):
        """
        Next fit
        """
        for task in self.tasks:
            if not self.can_be_placed(task, self.last_core_used):
                self.can_be_partitioned = False

    def du(self):
        """
        Decreasing utilisation
        """
        self.tasks.sort(key=lambda task: task.utilization, reverse=True)

    def iu(self):
        """
        Increasing utilisation
        :return:
        """
        self.tasks.sort(key=lambda task: task.utilization)