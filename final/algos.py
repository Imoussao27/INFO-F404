from operator import attrgetter


class Algo:
    def __init__(self, tasks):
        self.tasks = tasks

    def getListJobs(self, feasibility):
        jobs = []
        for task in self.tasks:
            task.init_jobs(feasibility)
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

class RM(Algo):
    def __init__(self, tasks):
        self.tasks = tasks
        super().__init__(tasks)

    def run(self, scheduler):
        feasibility = self.feasibility()
        priority = self.listePriority(self.tasks)
        return scheduler.runXM(feasibility, priority)

    def listePriority(self, task):
        liste = self.getListPeriod(task)
        return self.getPriority(liste)

    def getListPeriod(self, tasks):
        listPeriod = []
        for element in tasks:
            listPeriod.append((element.period, element.id))
        return listPeriod

    def getPriority(self, liste):
        return super().getPriority(liste)

    def feasibility(self):
        return 256

    def priority(self):
        pass


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
        return 256



class EDF(Algo):
    def __init__(self, tasks):
        super().__init__(tasks)

    def feasibility(self):
        return 256

    def run(self, scheduler):
        feasibility = self.feasibility()
        return scheduler.runEDF(feasibility)