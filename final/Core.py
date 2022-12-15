from Scheduler import EDFScheduler


class Core:
    def __init__(self, id):
        """
        A core class containing a tasks set

        :param id: the core identifier and it is unique
        """
        self.id = id
        self.tasks = []
        self.utilization = 0
        self.scheduler = EDFScheduler(self.tasks) #TODO: call the good algo

    def __str__(self):
        res = ""
        for task in self.tasks:
            res += "T{} U{},".format(task.id, task.utilization)
        return "Core {} contains : ".format(self.id) + res[:-1]

    def add_task(self, task):
        self.tasks.append(task)
        self.utilization += task.getUtilization()

    def remove_task(self):
        task = self.tasks.pop()
        self.utilization -= task.getUtilization()

    def get_utilization(self):
        return self.utilization

    def get_tasks(self):
        return self.tasks

    def is_scheduling(self, limit):
        return self.scheduler.is_scheduling(limit)

    def schedule(self, limit):
        #TODO: appeler ici les algo with param
        self.scheduler.run(limit)
