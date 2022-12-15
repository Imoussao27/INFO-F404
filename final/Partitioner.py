from Core import *

class Partitioner:
    def __init__(self, tasks, heuristic, sort, limit, cores_number):
        self.heuristic = heuristic #ff wf bf nf
        self.sort = sort  #du iu
        self.limit = limit
        self.tasks = tasks #list of task
        self.cores = [Core(i + 1) for i in range(cores_number)]
        self.last_core_used = 0
        self.can_be_partitioned = True

    def is_partitioned(self):
        return self.can_be_partitioned

    def get_cores(self):
        return [core for core in self.cores if core.get_utilization() > 0]

    def can_be_placed(self, task, current):
        """
        Try to place a task in one of the cores starting from the current core

        :param task: the task to place
        :param current: the current core to use
        :return: True if the task can be placed in one of the cores otherwise False
        """
        it = current
        while it < len(self.cores):
            self.last_core_used = it
            self.cores[it].add_task(task)
            res = self.cores[it].is_scheduling(self.limit)
            task.reset()
            if not res:
                self.cores[it].remove_task()
                it += 1
            else:
                return True
        return False

    def ff_fit(self):
        """
        First fit
        """
        for task in self.tasks:
            if not self.can_be_placed(task, 0):
                self.can_be_partitioned = False

    def wf_fit(self):
        """
        Worst fit
        """
        for task in self.tasks:
            if not self.can_be_placed(task, 0):
                self.can_be_partitioned = False
            self.cores.sort(key=lambda partition: partition.utilization)

    def bf_fit(self):
        """
        Best fit
        """
        for task in self.tasks:
            if not self.can_be_placed(task, 0):
                self.can_be_partitioned = False
            self.cores.sort(key=lambda partition: partition.utilization, reverse=True)

    def nf_fit(self):
        """
        Next fit
        """
        for task in self.tasks:
            if not self.can_be_placed(task, self.last_core_used):
                self.can_be_partitioned = False

    def du(self):
        self.tasks.sort(key=lambda task: task.utilization, reverse=True)

    def iu(self):
        self.tasks.sort(key=lambda task: task.utilization)