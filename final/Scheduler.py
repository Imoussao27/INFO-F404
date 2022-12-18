import algos

class Scheduler:
    def __init__(self, tasks):
        self.tasks = tasks
        self.algo = algos.Algo(tasks)
        self.allTasks = []

    def isScheduling(self, lcm):
        """
        Verify if its scheduling
        :param lcm: int lcm
        :return: boolean True if its scheduling
        """
        time1 = self.algo.getOmax() + self.algo.getP()
        time2 = self.algo.getOmax() + self.algo.getP() * 2
        jobs = self.algo.getListJobs(lcm)

        for time in range(0, lcm + 1):
            if time == time1:
                configuration1 = self.getConfiguration(time1)
            elif time == time2:
                configuration2 = self.getConfiguration(time2)
                if configuration1 != configuration2:
                    return False

            running = False
            index = 0
            while not running and jobs and index < len(jobs):
                job = jobs[index]
                if self.verifyJob(job, lcm, time):
                    job.startJob()
                    if job.state:
                        jobs.pop(index)
                        if not time + 1 <= job.deadline:
                            return False
                    running = True

                index += 1
        return True

    def verifyJob(self, job, limit, time):
        return job.offset <= time and job.offset < limit and job.state != True

    def getConfiguration(self, time1):
        return [task.configuration(time1) for task in self.tasks]

    def init_run(self, limit):
        jobs = self.algo.getListJobs(limit)
        self.allTasks = {i: {"deadline miss": [], "job": []} for i in range(limit + 1)}
        return jobs

    def runAlgo(self, algo):
        self.algo = algo
        return self.algo.run(self)

    def runXM(self, feasibility, priority):
        """
        Schedule with RM and DM algo
        :param feasibility: int feasibility
        :param priority: list of priority of task
        :return: feasibility and list of task scheduling
        """

        jobs = self.init_run(feasibility)

        for time in range(feasibility):
            running = False
            index = 0  #index for the list of jobs
            while not running and jobs and index < len(jobs):
                p = 0 #index for the list of priority
                while p < len(priority) and not running:
                    job = jobs[index]
                    if job.task.id == priority[p] and job.offset <= time and job.offset < feasibility and job.state != True:
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
        """
        Schedule with RM and DM algo
        :param feasibility: int feasibility
        :return: feasibility and list of task scheduling
        """

        jobs = self.init_run(feasibility)

        for time in range(feasibility): # entre 0 et feasibility
            running = False
            index = 0
            while not running and jobs and index < len(jobs): # verify if its running or there is a jobs
                job = jobs[index]
                if self.verifyJob(job, feasibility, time):
                    running = self.runningJob(index, job, jobs, time)

                if job.deadline <= time: #Deadline miss
                    return self.deadlineMiss(feasibility, job, time)

                index += 1

        return feasibility, self.allTasks

    def deadlineMiss(self, feasibility, job, t):
        self.allTasks[t]["deadline miss"].append("{}".format(job.idToString()))
        return feasibility, self.allTasks

    def runningJob(self, index, job, jobs, time):
        """
        :param index: int index of job
        :param job: job
        :param jobs: list of jobs
        :param time:int time
        :return: True
        """
        self.allTasks[time]["job"].append("{}".format(job.idToString()))
        job.startJob()
        if job.state:
            jobs.pop(index)
        return True


