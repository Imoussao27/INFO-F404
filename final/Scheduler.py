from math import lcm
import algos

class Scheduler:
    def __init__(self, tasks):
        self.tasks = tasks
        self.algo = algos.Algo(tasks)
        self.allTasks = []

    def get_o_max(self):
        o_max = 0
        for task in self.tasks:
            if o_max < task.offset:
                o_max = task.offset
        return o_max

    def get_p(self):
        period_list = []
        for task in self.tasks:
            period_list.append(task.period)
        return lcm(*period_list)

    def get_configurations(self, t):
        return [task.configuration(t) for task in self.tasks]

    def is_scheduling(self, limit):
        t1 = self.get_o_max() + self.get_p()
        t2 = self.get_o_max() + self.get_p() * 2
        jobs = self.algo.getListJobs(limit)

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
                if job.offset <= t and job.offset < limit and job.state != True :
                    job.startJob()
                    if job.state == True :
                        jobs.pop(it)
                        if not t + 1 <= job.deadline:
                            return False
                    is_selected = True

                it += 1
        return True

 #----------------------------------------------OKAY------------------------------------

    def init_run(self, limit):
        jobs = self.algo.getListJobs(limit)
        self.allTasks = {i: {"deadline miss": [], "job": []} for i in range(limit + 1)}
        return jobs

    def runAlgo(self, algo):
        self.algo = algo
        return self.algo.run(self)

    def runXM(self, feasibility, priority):

        jobs = self.init_run(feasibility)

        for time in range(feasibility):
            running = False
            index = 0  #index for the list of jobs
            while not running and jobs and index < len(jobs):
                p = 0 #index for the list of priority
                while p < len(priority) and not running:
                    job = jobs[index]
                    if job.task.id == priority[p] and job.offset <= time and job.offset < feasibility and not job.state: #!= "Done"
                        running = self.runningJob(index, job, jobs, time)
                    elif job.deadline <= time:
                        return self.deadlineMiss(feasibility, job, time)
                    else:
                        index += 1

                    if index == len(jobs):
                        index = 0
                        p += 1

                index += 1

        return feasibility, self.allTasks

    def runEDF(self, feasibility):

        jobs = self.init_run(feasibility)

        for time in range(0, feasibility):
            running = False
            index = 0
            while not running and jobs and index < len(jobs):
                job = jobs[index]
                if job.offset <= time and job.offset < feasibility and not job.state:
                    running = self.runningJob(index, job, jobs, time)

                if job.deadline <= time:
                    return self.deadlineMiss(feasibility, job, time)

                index += 1

        return feasibility, self.allTasks

    def deadlineMiss(self, feasibility, job, t):
        self.allTasks[t]["deadline miss"].append("{}".format(job.idToString()))
        return feasibility, self.allTasks

    def runningJob(self, it, job, jobs, t):
        self.allTasks[t]["job"].append("{}".format(job.idToString()))
        job.startJob()
        if job.state:
            jobs.pop(it)
        return True


