from algorithm import *

class earliest_deadline_first(algorithm):
    def __init__(self, WCET, period):
        super().__init__(WCET, period)

    def run(self, lcm, tasks, order, numberOrder=1):
        feasibility = super().getFeasibility()
        isFeasibility = self.feasibilityIntervalEDF(feasibility)
        super().setIsFeasibility(isFeasibility)
        if isFeasibility:
            lcm = self.feasibility(self.WCET, self.period)
        return super().run(lcm, tasks, order, numberOrder)

    def feasibility(self, WCET, period):
        """
        Function handle the feasibility for earliest deadline first
        with this formula : Ci + Sum(wk / Ti) * Cj
        :param WCET: list of element of WCET
        :param period: list of element of period
        :return: feasibility interval for EDF
        """
        l = sum(WCET)
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