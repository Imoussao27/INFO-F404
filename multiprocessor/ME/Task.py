class Task:
    task_id: int
    offset: int
    wcet: int
    period: int
    deadline: int
    job_released: int = 0

    def __init__(self, task_id, offset, wcet,period, deadline):
        self.task_id = task_id
        self.offset = offset
        self.wcet = wcet
        self.period = period
        self.deadline = deadline

    def increase_job(self, time: int):
        self.job_released += 1

    def getOffset(self):
        return self.offset

    def getWcet(self):
        return self.wcet

    def getPeriod(self):
        return self.period

    def getDeadline(self):
        return self.deadline




