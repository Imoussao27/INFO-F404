from Core import *

class Partitioner:
    def __init__(self, tasks, heuristic, sort, limit, cores_number):
        self.heuristic = heuristic #ff wf bf nf
        self.sort = sort  #du iu
        self.limit = limit
        self.tasks = tasks #list of task
        self.cores = [Core(i + 1) for i in range(cores_number)]
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
            res = self.cores[copy_current].is_scheduling(self.limit) #verify scheduling
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