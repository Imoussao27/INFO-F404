import algos

class Scheduler:
    def __init__(self, tasks):
        self.tasks = tasks
        self.algo = algos.Algo(tasks)
        self.allTasks = []


    def is_scheduling(self, limit):
        t1 = self.algo.getOmax() + self.algo.getP()
        t2 = self.algo.getOmax() + self.algo.getP() * 2
        jobs = self.algo.getListJobs(limit)

        for t in range(0, limit + 1):
            if t == t1:
                conf1 = [task.configuration(t1) for task in self.tasks]
            elif t == t2:
                conf2 = [task.configuration(t2) for task in self.tasks]
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
                if time == 1:
                    print("times", time, "index", index)
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

                    if p == len(priority): #Evitez une boucle à l'infini
                        index = len(jobs)

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


