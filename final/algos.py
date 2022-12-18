from math import ceil, lcm
from operator import attrgetter

class Algo:
    def __init__(self, tasks):
        self.tasks = tasks

    def idleInstant(self):
        """
        Calcul the feasibiliry
        :return: int feasibility
        """
        wcet = self.getListWCET() # C
        period = self.getListPeriod() # T
        l = sum(wcet) #Sum(Ci)
        isFeasibility = False
        while not isFeasibility:
            lk = 0
            for i in range(len(period)):
                lk += ceil(l / period[i]) * wcet[i] #Sum(lk/Ti) * Ci
            if lk == l:
                isFeasibility = True
            l = lk

        return lk

    def getOmax(self):
        omax = 0
        for task in self.tasks:
            if omax < task.offset:
                omax = task.offset
        return omax #Get Omax

    def getP(self):
        period = self.getListPeriod()
        return lcm(*period) #Get P

    def isConstrained(self):
        """
        Verify if the system is constrained
        :return: boolean if the system is constrained
        """
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
        """
        Verify is the system is synchronous or Asynchronous
        :return: True if its Aynchronous
        """
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
        """
        Display the task job with their time
        :param feasibility: intn feasibility
        :param allTasks: list of task
        :return: None
        """
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
                        exit(4) #Deadline miss

    def feasibility(self):
        """
        Feasibility for RM and DM
        :return: int feasibility
        """
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
    """
    Scheduling algorithms rate monotonic
    """
    def __init__(self, tasks):
        self.tasks = tasks
        super().__init__(tasks)

    def run(self, scheduler):
        feasibility = self.feasibility()
        priority = self.listePriority(self.tasks)
        return scheduler.runXM(feasibility, priority) #Run scheduler

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
        feasi = super().feasibility()
        print("Feasibility : [ 0,", feasi, "]")
        return feasi


class DM(Algo):
    """
    Scheduling algorithms deadline monotonic
    """
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
        feasi = super().feasibility()
        print("Feasibility : [ 0,", feasi, "]")
        return feasi


class EDF(Algo):
    """
    Scheduling algorithms earliest deadline first
    """
    def __init__(self, tasks):
        super().__init__(tasks)

    def feasibility(self):
        if super().verifySynchronous():
            feasi = super().idleInstant()
        else:
            feasi = super().getOmax() + super().getP() * 2
        print("Feasibility : [ 0,", feasi, "]")
        return feasi + 1



    def run(self, scheduler):
        feasibility = self.feasibility()
        return scheduler.runEDF(feasibility)