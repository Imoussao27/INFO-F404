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
