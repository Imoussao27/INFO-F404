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
        """
        Add a task to the core tasks list

        :param task: the task to be added
        """
        self.tasks.append(task)
        self.utilization += task.get_utilization()

    def remove_task(self):
        """
        Remove the last added task to the core tasks list
        """
        task = self.tasks.pop()
        self.utilization -= task.get_utilization()

    def get_utilization(self):
        """
        Get the sum of all the tasks utilization

        :return: sum of the utilization
        """
        return self.utilization

    def get_tasks(self):
        """
        Get all the tasks contained in the core

        :return: the list of the tasks
        """
        return self.tasks

    def is_scheduling(self, limit):
        """
        Try to schedule the core

        :param limit: the time step limit for the simulator
        :return: True if the core can be schedule
        """
        return self.scheduler.is_scheduling(limit)

    def schedule(self, limit):
        """
        Run the simulation of the scheduling of the core

        :param limit: the time step limit for the simulator
        """
        self.scheduler.run(limit)
