class Job:
    def __init__(self, task, id):
        """
        The class of a periodic task job

        :param task: the job proprietary task
        :param id: the job identifier and it is unique
        """
        self.task = task
        self.id = id
        self.offset = task.offset + (id - 1) * task.period
        self.wcet = task.wcet
        self.deadline = task.offset + (id - 1) * task.period + task.deadline
        self.state = "Undone"
        self.time_remaining = self.wcet

    def get_task(self):
        return self.task

    def get_id(self):
        return "T{}J{}".format(self.task.id, self.id)

    def get_offset(self):
        return self.offset

    def get_deadline(self):
        return self.deadline

    def get_cumulative_time(self):
        return self.wcet - self.time_remaining

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def is_deadline_met(self, t):
        return t + 1 <= self.deadline

    def decrease(self):
        self.time_remaining -= 1

    def run(self):
        """
        Run the job execution
        """
        self.decrease()
        self.task.setOldest_active_job(self)
        if self.state == "Undone":
            self.task.increaseActive_jobs()
            self.state = "Running"

    def stop(self):
        """
        Stop the job execution
        """
        if self.time_remaining == 0:
            self.set_state("Done")
            self.task.decreaseActive_jobs()
            if self.task.getOldest_active_job().get_id() == self.id:
                self.task.setOldest_active_job(None)

class Task:
    def __init__(self, id, offset, wcet, deadline, period):
        """
        The class of a periodic task

        :param id: the task identifier and it is unique
        :param offset: the release time of the first job of the task
        :param wcet: the worst-case execution requirement of the task
        :param deadline: the time-delay between a job release and the corresponding deadline of the task
        :param period: the duration between two consecutive task releases
        """
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
        """
        Initialise the set of jobs for the periodic task in the interval [0,limit]

        :param limit: the time step limit for the simulator
        """
        self.jobs = []
        k = 1
        while self.offset + (k - 1) * self.period <= limit:
            self.jobs.append(Job(self, k))
            k += 1

    def getPeriod(self):
        return self.period

    def getUtilization(self):
        return self.utilization

    def getJobs(self):
        return self.jobs

    def getActive_jobs(self):
        return self.active_jobs

    def getOldest_active_job(self):
        return self.oldest_active_job

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
        """
        Define the configuration at instant t as follows:
            - gamma: the time elapsed since the request of the task
            - alpha: the number of active jobs
            - beta: the cumulative CPU time used by the oldest active job of the task

        :param t: instant t
        :return: a tuple of (gamma, alpha, beta)
        """
        gamma = (t - self.offset) % self.period if t >= self.offset else t - self.offset
        alpha = self.active_jobs
        beta = 0 if alpha == 0 else self.oldest_active_job.get_cumulative_time()

        return gamma, alpha, beta