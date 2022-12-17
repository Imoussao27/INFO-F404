class Job:
    def __init__(self, task, id):
        self.task = task
        self.id = id
        self.offset = task.offset + (id - 1) * task.period
        self.wcet = task.wcet
        self.deadline = task.offset + (id - 1) * task.period + task.deadline
        self.state = False
        self.time_remaining = self.wcet

    def idToString(self):
        return "T{}J{}".format(self.task.id, self.id)

    def get_cumulative_time(self):
        return self.wcet - self.time_remaining

    def decrease(self):
        self.time_remaining -= 1

    def startJob(self):
        self.decrease()
        self.task.setOldest_active_job(self)
        if self.state == False:
            self.task.increaseActive_jobs()
            self.state = None

        #STOP JOB
        if self.time_remaining == 0:
            self.state = True
            self.task.decreaseActive_jobs()
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

    def increaseActive_jobs(self):
        self.active_jobs += 1

    def decreaseActive_jobs(self):
        self.active_jobs -= 1

    def reset(self):
        self.active_jobs = 0
        self.oldest_active_job = None

    def configuration(self, t):
        gamma = (t - self.offset) % self.period if t >= self.offset else t - self.offset
        alpha = self.active_jobs
        beta = 0 if alpha == 0 else self.oldest_active_job.get_cumulative_time()

        return gamma, alpha, beta