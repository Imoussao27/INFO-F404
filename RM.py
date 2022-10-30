from tools import *
from math import *
class rate_monotonic:
    def __init__(self, WCET, period):
        self.listRateMonotonic = []
        self.tool = tools()
        self.WCET = WCET
        self.period = period

    def run(self, lcm, tasks, order):
        feasibility = self.tool.feasibilityInterval(self.WCET, self.period)
        isFeasibility = self.feasibilityIntervalRM(feasibility)
        if not isFeasibility:
            print("MISSING TASK")
        #    exit(1)
        print("Feasibility interval is [ 0,", lcm,"]")
        return self.algorithm(lcm, tasks, order)

    def feasibilityIntervalRM(self, feasibility):
        if (feasibility <= 0.69):
            return True
        elif (feasibility >= 0.69 and feasibility <= 1):
            return self.feasibility(self.WCET, self.period)
        else:
            return False

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
            if(oldSomme > max(self.period)):
                return False
        print(oldSomme)
        return isFeasibility

    def addNewTask(self, listOfTimes, tasks, order):
        """
        Add task in list
        :param listOfTimes: list of deadline of job
        :param tasks: list of task
        :return: a list of task ongoing
        """
        tasksOnGoing = [[] for i in range(len(tasks))]
        for i in range(len(tasks)):
            if (tasks[i] != []):
                tasksOnGoing[i].append(listOfTimes[i])
                tasksOnGoing[i].append(tasks[i][0][0])
                tasksOnGoing[i].append(tasks[i][0][1])
                name = "T" + str(i + 1)
                tasksOnGoing[i].append(name)
                tasksOnGoing[i].append(order.index(name))
        return tasksOnGoing

    def algorithm(self, lcm, tasks, order):
        listOfTimes = [0 for i in range(len(tasks))]
        countOfJob = self.tool.copyList(self.WCET)
        time = 0
        tasksOnGoing = self.addNewTask(listOfTimes, tasks, order)  # list of list with period and name of task

        while (len(tasksOnGoing) != 0) and (lcm >= time):  # while there's not task
            onGoing = []
            for index in range(len(tasksOnGoing)):
                if (tasksOnGoing[index] != []):
                    if (tasksOnGoing[index][0] <= time):
                        onGoing.append(tasksOnGoing[index])

                    if (tasksOnGoing[index][1] <= time):
                        return self.listRateMonotonic

            newTasksOnGoing = []
            for element in tasksOnGoing:
                if element not in onGoing:
                    newTasksOnGoing.append(element)
            tasksOnGoing = newTasksOnGoing

            if (len(onGoing) != 0):
                onGoing.sort(key=lambda a: a[4])  # sort task by priority onGoing
                job = onGoing[0][3]
                index = int(job[1]) - 1
                tasks[index].remove((int(onGoing[0][1]), int(onGoing[0][2])))
                countOfJob[index] -= 1
                if countOfJob[index] == 0:
                    listOfTimes[index] = int(onGoing[0][1])
                    countOfJob[index] = self.WCET[index]
                self.listRateMonotonic.append((job, time + 1))
                time += 1
                del onGoing[0]
            else:
                tasksOnGoingEmpty = [[] for i in range(len(tasksOnGoing))]
                if (tasksOnGoing == tasksOnGoingEmpty):
                    break
                else:
                    time += 1
            tasksOnGoing = self.addNewTask(listOfTimes, tasks, order)
        return self.listRateMonotonic
