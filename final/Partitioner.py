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

    def ff_fit(self):
        """
        First fit
        """
        for task in self.tasks:
            if not self.can_be_placed(task, 0):
                self.can_be_partitioned = False

    def wf_fit(self):
        """
        Assign the task τi on the processor with the lowest utilisation factor able to accept it
        """
        for task in self.tasks:
            if not self.can_be_placed(task, 0):
                self.can_be_partitioned = False
            self.sort_cores("wf")

    def bf_fit(self):
        """
        Assign the task τi on the first processor with the highest utilisation factor able to accept it
        """
        for task in self.tasks:
            if not self.can_be_placed(task, 0):
                self.can_be_partitioned = False
            self.sort_cores("bf")

    def nf_fit(self):
        """
        Only the last cores used can receive tasks. When it is not possible to place the task τi, the current
        core is closed (it will no longer be able to receive new tasks). The next cores then becomes the new
        current core.
        """
        for task in self.tasks:
            if not self.can_be_placed(task, self.last_core_used):
                self.can_be_partitioned = False

