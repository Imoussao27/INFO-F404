from algorithm import *

class rate_monotonic(algorithm):
    def __init__(self, WCET, period):
        self.numberOfTask = self.size = len(WCET)
        super().__init__(WCET, period)


    def run(self, lcm, tasks, order, numberOrder=4):
        feasibility = super().getFeasibility()
        isFeasibility = self.feasibilityIntervalRM(feasibility)
        super().setIsFeasibility(isFeasibility)
        return super().run(lcm, tasks, order, numberOrder)


    def feasibilityIntervalRM(self, feasibility):  # TODO: verify ce que aissa a dit, also pour edf
        if (feasibility <= 0.69):
            return True
        elif (feasibility >= 0.69 and feasibility <= 1):
            return self.feasibility(self.WCET, self.period)
        # else:
        #    return False

    def feasibility(self, WCET, period):
        """
        Function handle the feasibility for rate monotonic
        with this formula : Ci + Sum(wk / Ti) * Cj
        :param WCET: list of element of WCET
        :param period: list of element of period
        :return: True if the system is feasibility
        """
        oldSomme = 0
        isFeasibility = False
        for i in range(len(WCET)):
            isFeasibility = False
            w2 = WCET[i]  # Ci
            beforeWT = WCET[i]  # wk
            while not isFeasibility and oldSomme <= max(self.period):
                for j in range(len(WCET)):
                    somme = 0  # wk+1
                    for k in range(i):
                        wt = ceil(beforeWT / period[k]) * WCET[k]
                        somme += wt  # Sum(wk/Tj) * Cj
                    somme += w2  # (Sum(wk/Tj) * Cj) + Ci
                    beforeWT = somme
                    if (oldSomme == somme):  # verify if the system is feasible
                        isFeasibility = True
                        break
                    oldSomme = somme
            if (oldSomme > max(self.period)):
                return False
        return isFeasibility


    def visualization(self, lcm, listAllTasks, name):
        super().visualizationTool(lcm, listAllTasks, self.size, self.numberOfTask, name)