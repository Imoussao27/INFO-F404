from algorithm import *
from math import *

class earliest_deadline_first(algorithm):
    def __init__(self, WCET, period):
        self.numberOfTask = self.size = len(WCET)
        super().__init__(WCET, period)

    def run(self, tasks, order, numberOrder=1):
        """
        :param tasks: list of tasks
        :param order: priority of job
        :param numberOrder: number to order list
        :return: a list of task ongoing
        """
        feasibility = super().getFeasibility()
        isFeasibility = self.feasibilityIntervalEDF(feasibility)
        if isFeasibility:
            self.feasi = self.feasibility(self.WCET, self.period)
        super().setIsFeasibility(isFeasibility)
        return super().run(tasks, order, numberOrder)

    def feasibility(self, WCET, period):
        """
        Function handle the feasibility for earliest deadline first
        with this formula : Ci + Sum(wk / Ti) * Cj
        :param WCET: list of element of WCET
        :param period: list of element of period
        :return: feasibility interval for EDF
        """
        print(period)
        l = sum(WCET)
        print(l)
        isFeasibility = False
        while not isFeasibility:
            lk = 0
            for i in range(len(period)):
                lk += ceil(l / period[i]) * WCET[i]
            if lk == l:
                isFeasibility = True
            l = lk
        return lk

    def feasibilityIntervalEDF(self, feasibility):
        if feasibility <= 1:
            return True
        else:
            return False  # not schedule

    def visualization(self, listAllTasks, name):
        super().visualizationTool(listAllTasks, self.size, self.numberOfTask, name)