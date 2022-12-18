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
        self.task.setOldestJob(self)
        if self.state == False:
            self.task.active_jobs += 1
            self.state = None

        #STOP JOB
        if self.timeWCET == 0:
            self.state = True
            self.task.active_jobs -= 1
            if self.task.oldestJob.idToString() == self.id:
                self.task.setOldestJob(None)

class Task:
    def __init__(self, id, offset, wcet, deadline, period):
        self.id = id
        self.offset = offset
        self.wcet = wcet
        self.deadline = deadline
        self.period = period
        self.utilization = wcet / period
        self.active_jobs = 0
        self.oldestJob = None
        self.jobs = []

    def initJobs(self, limit):
        self.jobs = []
        i = 1
        while self.offset + (i - 1) * self.period <= limit:
            self.jobs.append(Job(self, i))
            i += 1

    def setOldestJob(self, job):
        if not self.oldestJob:
            self.oldestJob = job

    def reset(self):
        self.active_jobs = 0
        self.oldestJob = None

    def getGamma(self, time):
        if time >= self.offset:
            return (time - self.offset) % self.period
        return time - self.offset

    def getBeta(self):
        if self.active_jobs == 0:
            return 0
        return self.oldestJob.getAllTime()

    def configuration(self, time):
        return self.getGamma(time), self.active_jobs, self.getBeta()