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

    def __str__(self):
        return self.id + "\noffset {}\nWCET {}\ndeadline {}".format(self.offset, self.wcet, self.deadline)

    def get_task(self):
        """
        Get the job proprietary task

        :return: the job proprietary task
        """
        return self.task

    def get_id(self):
        """
        Get the job identifier

        :return: job ID
        """
        return "T{}J{}".format(self.task.id, self.id)

    def get_offset(self):
        """
        Get the job offset

        :return: the job offset
        """
        return self.offset

    def get_deadline(self):
        """
        Get the job deadline

        :return: the job deadline
        """
        return self.deadline

    def get_cumulative_time(self):
        """
        Get the cumulative CPU time used by the job

        :return: the cumulative CPU time
        """
        return self.wcet - self.time_remaining

    def get_state(self):
        """
        Get the execution state of the job

        :return: job state
        """
        return self.state

    def set_state(self, state):
        """
        Set the execution state of the job

        :param state: the current execution state of the job
        """
        self.state = state

    def is_deadline_met(self, t):
        """
        Get if the deadline is met

        :return: True if the deadline is met otherwise False
        """
        return t + 1 <= self.deadline

    def decrease(self):
        """
        Decrease the remaining CPU time to be used by the job
        """
        self.time_remaining -= 1

    def run(self):
        """
        Run the job execution
        """
        self.decrease()
        self.task.set_oldest_active_job(self)
        if self.state == "Undone":
            self.task.increase_active_jobs()
            self.state = "Running"

    def stop(self):
        """
        Stop the job execution
        """
        if self.time_remaining == 0:
            self.set_state("Done")
            self.task.decrease_active_jobs()
            if self.task.get_oldest_active_job().get_id() == self.id:
                self.task.set_oldest_active_job(None)
