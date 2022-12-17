from math import lcm
from operator import attrgetter


class Scheduler:
    def __init__(self, tasks):
        self.tasks = tasks
        self.allTasks = []

    def sort_all_jobs(self, limit):
        jobs = []
        for task in self.tasks:
            task.init_jobs(limit)
            jobs += task.getJobs()
        return sorted(jobs, key=attrgetter('deadline', 'offset'))

    def get_o_max(self):
        o_max = 0
        for task in self.tasks:
            if o_max < task.offset:
                o_max = task.offset
        return o_max

    def get_p(self):
        period_list = []
        for task in self.tasks:
            period_list.append(task.getPeriod())
        return lcm(*period_list)

    def get_configurations(self, t):
        return [task.configuration(t) for task in self.tasks]

    def is_scheduling(self, limit):
        t1 = self.get_o_max() + self.get_p()
        t2 = self.get_o_max() + self.get_p() * 2
        jobs = self.sort_all_jobs(limit)

        for t in range(0, limit + 1):
            if t == t1:
                conf1 = self.get_configurations(t1)
            elif t == t2:
                conf2 = self.get_configurations(t2)
                if conf1 != conf2:
                    return False

            is_selected, it = False, 0
            while not is_selected and jobs and it < len(jobs):
                job = jobs[it]
                if job.offset <= t and job.offset < limit and job.get_state() != True :#!= "Done":
                    job.run()
                    job.stop()
                    if job.get_state() == True :#== "Done":
                        jobs.pop(it)
                        if not job.is_deadline_met(t):
                            return False
                    is_selected = True

                it += 1
        return True

    def getListPeriod(self):
        listPeriod = []
        for element in self.tasks:
            listPeriod.append((element.period, element.id))
        return listPeriod

    def getListDealine(self):
        listDealine = []
        for element in self.tasks:
            listDealine.append((element.deadline, element.id))
        return listDealine


    def getPriority(self, liste):
        priority = []
        liste.sort(key=lambda x: x[0])
        for element in liste:
            priority.append(element[1])
        return priority

    def init_run(self, limit):
        jobs = self.sort_all_jobs(limit)
        self.allTasks = {i: {"deadline miss": [], "job": []} for i in range(limit + 1)}
        priority = self.getPriority(self.getListPeriod())
        return jobs, priority


    def runtest(self, feasibility):

        jobs, priority = self.init_run(feasibility)

        #TODO: POUR RM -> PERIOD (but demander pour etre sure)
        #TODO: POUR DM -> DEADLINE

        for t in range(feasibility):
            running = False
            index = 0  #index for the list of jobs
            while not running and jobs and index < len(jobs):
                p = 0 #index for the list of priority
                while p < len(priority) and not running: #TODO: VOIR SI ON PEUT CREER UNE FUNCTION
                    job = jobs[index]
                    if job.task.id == priority[p] and job.offset <= t and job.offset < feasibility and not job.get_state(): #!= "Done"
                        self.allTasks[t]["job"].append("{}".format(job.get_id()))
                        job.run()
                        job.stop()
                        if job.get_state(): # == "Done":
                            jobs.pop(index)
                        running = True

                    elif job.deadline <= t:
                        self.allTasks[t]["deadline miss"].append("{}".format(job.get_id()))
                        return self.print_timeline(feasibility)
                    else:
                        index += 1


                    if index == len(jobs):
                        index = 0
                        p += 1


                index += 1

        return self.print_timeline(feasibility)



    def run(self, limit):
        """
        Simulate the execution of the EDF scheduler on the core's tasks set

        :param limit: the time step feasibility for the simulator
        """
        jobs = self.sort_all_jobs(limit)
        self.allTasks = {i: {"release": [], "deadline": [], "running": []} for i in range(limit + 1)}


        for t in range(0, limit + 1):
            is_selected = False
            it = 0
            while not is_selected and jobs and it < len(jobs):
                job = jobs[it]
                if job.offset <= t and job.offset < limit and job.get_state() != "Done":
                    self.allTasks[t]["running"].append("{}".format(job.get_id()))
                    job.run()
                    job.stop()
                    if job.get_state() == "Done":
                        jobs.pop(it)
                    is_selected = True

                it += 1

        self.print_timeline(limit)

    def print_timeline(self, feasibility):
        task = ""
        oldtime = 0
        for time in range(feasibility + 1):
            for status in self.allTasks[time]:
                for element in self.allTasks[time][status]:
                    if task == "":
                        task = element
                        oldtime = time
                    elif task != element:
                        print(task + " ["+ str(oldtime) +" , "+ str(time) +"]")
                        task = element
                        oldtime = time
                    if status == "deadline miss":
                        print(status, element)
