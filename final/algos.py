from math import ceil, lcm
from operator import attrgetter

class Algo:
    def __init__(self, tasks):
        self.tasks = tasks

    def idleInstant(self):
        wcet = self.getListWCET()
        period = self.getListPeriod()
        l = sum(wcet)
        isFeasibility = False
        while not isFeasibility:
            lk = 0
            for i in range(len(period)):
                lk += ceil(l / period[i]) * wcet[i]
            if lk == l:
                isFeasibility = True
            l = lk
        return lk

    def getOmax(self):
        omax = 0
        for task in self.tasks:
            if omax < task.offset:
                omax = task.offset
        return omax

    def getP(self):
        period = self.getListPeriod()
        return lcm(*period)

    def isConstrained(self):
        deadline = self.getListDeadline()
        period = self.getListPeriod()

        for i in range(len(deadline)):
            if deadline[i] > period[i]:
                return False
        return True

    def getMaxDeadline(self):
        deadline = self.getListDeadline()
        return max(deadline)

    def getListOffset(self):
        offset = []
        for element in self.tasks:
            offset.append(element.offset)
        return offset

    def getListWCET(self):
        wcet = []
        for element in self.tasks:
            wcet.append(element.wcet)
        return wcet

    def getListPeriod(self):
        period = []
        for element in self.tasks:
            period.append(element.period)
        return period

    def getListDeadline(self):
        deadline = []
        for element in self.tasks:
            deadline.append(element.deadline)
        return deadline

    def verifySynchronous(self):
        offset = []
        for element in self.tasks:
            offsetValue = element.offset
            if offset != []:
                if offsetValue not in offset: #Asynchronous
                    return False
            offset.append(offsetValue)
        return True

    def getListJobs(self, feasibility):
        jobs = []
        for task in self.tasks:
            task.initJobs(feasibility)
            jobs += task.jobs
        return sorted(jobs, key=attrgetter('deadline', 'offset'))

    def getPriority(self, liste):
        priority = []
        liste.sort(key=lambda x: x[0])
        for element in liste:
            priority.append(element[1])
        return priority

    def toPrint(self, feasibility, allTasks):
        task = ""
        oldtime = 0
        for time in range(feasibility + 1):
            for status in allTasks[time]:
                for element in allTasks[time][status]:
                    if task == "":
                        task = element
                        oldtime = time
                    elif task != element:
                        print(task + " [" + str(oldtime) + " , " + str(time) + "]")
                        task = element
                        oldtime = time
                    if status == "deadline miss":
                        print(status, element)
                        exit(4)

    def feasibility(self):
        if self.verifySynchronous():
            if self.isConstrained():
                return self.getMaxDeadline() + 1
            else:
                return self.idleInstant() + 1

        else:
            if self.isConstrained():
                print('Asynchronous constrained')
                return sum(self.getListOffset()) + self.getP() + 1
            else:
                print("/!/ Asyncrhonous arbitrary /!/")
                exit(2)


class RM(Algo):
    def __init__(self, tasks):
        self.tasks = tasks
        super().__init__(tasks)

    def run(self, scheduler):
        feasibility = self.feasibility()
        priority = self.listePriority(self.tasks)
        return scheduler.runXM(feasibility, priority)

    def listePriority(self, task):
        liste = self.getListPeriodWithID(task)
        return self.getPriority(liste)

    def getListPeriodWithID(self, tasks):
        listPeriod = []
        for element in tasks:
            listPeriod.append((element.period, element.id))
        return listPeriod

    def getPriority(self, liste):
        return super().getPriority(liste)

    def feasibility(self):
        return super().feasibility()


class DM(Algo):
    def __init__(self, tasks):
        self.tasks = tasks
        super().__init__(tasks)

    def run(self, scheduler):
        feasibility = self.feasibility()
        priority = self.listePriority(self.tasks)
        return scheduler.runXM(feasibility, priority)

    def listePriority(self, task):
        liste = self.getListDealine(task)
        return self.getPriority(liste)

    def getListDealine(self, tasks):
        listDealine = []
        for element in tasks:
            listDealine.append((element.deadline, element.id))
        return listDealine

    def getPriority(self, liste):
        return super().getPriority(liste)

    def feasibility(self):
        return super().feasibility()


class EDF(Algo):
    def __init__(self, tasks):
        super().__init__(tasks)

    def feasibility(self):
        if super().verifySynchronous():
            return super().idleInstant() + 1
        else:
            feasi = super().getOmax() + super().getP() * 2
            return feasi + 1

    def run(self, scheduler):
        feasibility = self.feasibility()
        return scheduler.runEDF(feasibility)