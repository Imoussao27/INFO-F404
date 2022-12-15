from Core import *


class Partitioner:
    def __init__(self, tasks, heuristic, sort, limit, cores_number):
        """
        A partitioner class whose purpose is to partition the task set between the different cores according to a
        combination of sorting order and heuristic

        :param tasks: the list of tasks to be partitioned
        :param heuristic: the partitioning algorithm to use,
                    - "ff" : first fit
                    - "wf" : worst fit
                    - "bf" : best fit
                    - "nf" : next fit
        :param sort: the sorting algorithm to use,
                    - "du" : decreasing utilization
                    - "iu" : increasing utilization
        :param limit: the time step limit for the simulator
        :param cores_number: the number of identical cores
        """
        self.heuristic = heuristic #ff wf bf nf
        self.sort = sort  #du iu
        self.limit = limit
        self.tasks = tasks #list of task
        self.cores = [Core(i + 1) for i in range(cores_number)]
        self.last_core_used = 0
        self.can_be_partitioned = True

    def is_partitioned(self):
        """
        Get if the partitioner can partition the task set according to the given combination

        :return: True there is a partition otherwise False
        """
        return self.can_be_partitioned

    def get_cores(self):
        """
        Get the cores obtained after the partition

        :return: the list of the cores
        """
        return [core for core in self.cores if core.get_utilization() > 0]

    def sort_cores(self, sort):
        """
        Sorts the cores in a given order, the result is an ordered list of cores

        :param sort: the sorting algorithm to use,
                    - "bf" : the highest utilisation factor
                    - "wf" : the lowest utilisation factor
        """
        if sort == "bf":
            self.cores.sort(key=lambda partition: partition.utilization, reverse=True)
        elif sort == "wf":
            self.cores.sort(key=lambda partition: partition.utilization)

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

    def first_fit(self):
        """
        Assign the task τi on the first processor able to accept it, in the order of their indexes
        """
        for task in self.tasks:
            if not self.can_be_placed(task, 0):
                self.can_be_partitioned = False

    def worst_fit(self):
        """
        Assign the task τi on the processor with the lowest utilisation factor able to accept it
        """
        for task in self.tasks:
            if not self.can_be_placed(task, 0):
                self.can_be_partitioned = False
            self.sort_cores("wf")

    def best_fit(self):
        """
        Assign the task τi on the first processor with the highest utilisation factor able to accept it
        """
        for task in self.tasks:
            if not self.can_be_placed(task, 0):
                self.can_be_partitioned = False
            self.sort_cores("bf")

    def next_fit(self):
        """
        Only the last cores used can receive tasks. When it is not possible to place the task τi, the current
        core is closed (it will no longer be able to receive new tasks). The next cores then becomes the new
        current core.
        """
        for task in self.tasks:
            if not self.can_be_placed(task, self.last_core_used):
                self.can_be_partitioned = False

    def run(self):
        """
        Run the execution of the partitioner according to the given combination
        """
        if self.sort == "du":
            self.tasks.sort(key=lambda task: task.utilization, reverse=True)
        elif self.sort == "iu":
            self.tasks.sort(key=lambda task: task.utilization)

        if self.heuristic == "ff":
            self.first_fit()
        elif self.heuristic == "wf":
            self.worst_fit()
        elif self.heuristic == "bf":
            self.best_fit()
        elif self.heuristic == "nf":
            self.next_fit()
