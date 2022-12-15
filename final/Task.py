from Job import *


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

    def __str__(self):
        return "Task number {}\noffset {}\nWCET {}\ndeadline {}\nperiod {}".format(self.id, self.offset, self.wcet,
                                                                                   self.deadline, self.period)

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

    def get_offset(self):
        """
        Get the task offset

        :return: the task offset
        """
        return self.offset

    def get_deadline(self):
        """
        Get the task deadline

        :return: the task deadline
        """
        return self.deadline

    def get_period(self):
        """
        Get the task period

        :return: the task period
        """
        return self.period

    def get_utilization(self):
        """
        Get the task utilization (represent the division of wcet by the period)

        :return: the task utilization
        """
        return self.utilization

    def get_jobs(self):
        """
        Get all jobs generated from the task

        :return: the list of the jobs
        """
        return self.jobs

    def get_active_jobs(self):
        """
        Get the number of the active jobs during the simulation

        :return: the active jobs number
        """
        return self.active_jobs

    def get_oldest_active_job(self):
        """
        Get the oldest active job of the task at this moment of the simulation

        :return: the oldest active job of the task
        """
        return self.oldest_active_job

    def set_oldest_active_job(self, job):
        """
        set the job as the oldest active job in the task at this moment of the simulation

        :param job: the oldest job
        """
        if not self.oldest_active_job:
            self.oldest_active_job = job

    def increase_active_jobs(self):
        """
        Increase the number of the active jobs
        """
        self.active_jobs += 1

    def decrease_active_jobs(self):
        """
        Decrease the number of the active jobs
        """
        self.active_jobs -= 1

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

    def reset(self):
        """
        Reset some fields of the task
        """
        self.active_jobs = 0
        self.oldest_active_job = None
