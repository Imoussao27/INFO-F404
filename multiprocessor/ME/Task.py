class sous_job:
    id_job: int = 0
    id_sous_job: int = 0
    begin_time: int

    def __init__(self, id_job, id_sous_job, begin_time):
        self.id_job = id_job
        self.id_sous_job = id_sous_job
        self.begin_time = begin_time

class job:
    id_job: int = 0
    id_task: int = 0
    sous_job_list: list = []

    def __init__(self, id_job, id_task):
        self.id_job = id_job
        self.id_task = id_task

    def addJob(self, sous_job):
        self.sous_job_list.append(sous_job)


class Task:
    id: int
    offset: int
    wcet: int
    deadline: int
    period: int
    count_wcet: int
    id_job: int = 0
    isDone: bool = False
    nextPeriod: int


    def __init__(self, id, offset, wcet, deadline, period):
        self.id = id
        self.offset = offset
        self.wcet = wcet
        self.deadline = deadline
        self.period = period

    def status(self):
        self.isDone = True

    def sousTask(self, offset, deadline):
        return Task(self.id, offset, self.wcet, deadline, deadline)

    def ToString(self):
        print(self.id, "|", self.offset, self.wcet, self.period, self.deadline)