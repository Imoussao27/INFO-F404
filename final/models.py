class Job:
    def __init__(self, task, id):
        self.task = task
        self.id = id
        self.offset = self.initOffset()
        self.wcet = task.wcet
        self.deadline = self.initDeadline()
        self.period = task.period
        self.timeWCET = self.wcet
        self.state = False


    def idToString(self):
        return "T{}J{}".format(self.task.id, self.id)

    def getAllTime(self):
        return self.wcet - self.timeWCET

    def initOffset(self):
        return self.task.offset + (self.id - 1) * self.task.period

    def initDeadline(self):
        return self.task.offset + (self.id - 1) * self.task.period + self.task.deadline

    def startJob(self):
        self.timeWCET -= 1
        self.task.setOldest_active_job(self)
        if self.state == False:
            self.task.active_jobs += 1
            self.state = None

        #STOP JOB
        if self.timeWCET == 0:
            self.state = True
            self.task.active_jobs -= 1
            if self.task.oldest_active_job.idToString() == self.id:
                self.task.setOldest_active_job(None)

class Task:
    def __init__(self, id, offset, wcet, deadline, period):
        self.id = id
        self.offset = offset
        self.wcet = wcet
        self.deadline = deadline
        self.period = period
        self.utilization = wcet / period
        self.active_jobs = 0
        self.oldest_active_job = None
        self.jobs = []

    def init_jobs(self, limit):
        self.jobs = []
        i = 1
        while self.offset + (i - 1) * self.period <= limit:
            self.jobs.append(Job(self, i))
            i += 1

    def setOldest_active_job(self, job):
        if not self.oldest_active_job:
            self.oldest_active_job = job

    def reset(self):
        self.active_jobs = 0
        self.oldest_active_job = None

    def configuration(self, t):
        gamma = (t - self.offset) % self.period if t >= self.offset else t - self.offset
        alpha = self.active_jobs
        beta = 0 if alpha == 0 else self.oldest_active_job.getAllTime()

        return gamma, alpha, beta