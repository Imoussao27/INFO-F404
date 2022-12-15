from math import lcm
from operator import attrgetter


class EDFScheduler:
    def __init__(self, tasks):
        """
        A scheduler class that can schedules the jobs of core with the EDF (earliest deadline first) strategy

        :param tasks: the list of the tasks
        """
        self.tasks = tasks
        self.timeline = []

    def sort_all_jobs(self, limit):
        """
        Sorting the core's jobs in an increasing way using the (deadline, offset) key

        :param limit: the time step limit for the simulator
        :return: an ordered list of all the core's jobs
        """
        jobs = []
        for task in self.tasks:
            task.init_jobs(limit)
            jobs += task.getJobs()
        return sorted(jobs, key=attrgetter('deadline', 'offset'))

    def get_o_max(self):
        """
        Get the maximum tasks set offset value

        :return: the maximum offset
        """
        o_max = 0
        for task in self.tasks:
            if o_max < task.offset:
                o_max = task.offset
        return o_max

    def get_p(self):
        """
        Get the hyper-period of the tasks set

        :return: the hyper-period
        """
        period_list = []
        for task in self.tasks:
            period_list.append(task.getPeriod())
        return lcm(*period_list)

    def get_configurations(self, t):
        """
        Get the configuration of the tasks set at instant t

        :param t: instant t
        :return: the list of configurations of the tasks set
        """
        return [task.configuration(t) for task in self.tasks]

    def is_scheduling(self, limit):
        """
        Try to schedule the jobs of a core

        :param limit: the time step limit for the simulator
        :return: True if the jobs of a core can be scheduled otherwise False
        """
        o_max, p = self.get_o_max(), self.get_p()
        t1, t2 = o_max + p, o_max + p * 2
        jobs = self.sort_all_jobs(limit)
        for t in range(0, limit + 1):
            if t == t1:
                conf1 = self.get_configurations(t1)
            elif t == t2:
                conf2 = self.get_configurations(t2)
                if conf1 != conf2:
                    return False

            is_selected, it = False, 0
            while not is_selected and jobs and it < len(jobs):
                job = jobs[it]
                if job.offset <= t and job.offset < limit and job.get_state() != "Done":
                    job.run()
                    job.stop()
                    if job.get_state() == "Done":
                        jobs.pop(it)
                        if not job.is_deadline_met(t):
                            return False
                    is_selected = True

                it += 1
        return True

    def run(self, limit):
        """
        Simulate the execution of the EDF scheduler on the core's tasks set

        :param limit: the time step limit for the simulator
        """
        jobs = self.sort_all_jobs(limit)
        self.timeline = {i: {"release": [], "deadline": [], "running": []} for i in range(limit + 1)}

        for t in range(0, limit + 1):
            is_selected, it = False, 0
            while not is_selected and jobs and it < len(jobs):
                job = jobs[it]
                if job.offset <= t and job.offset < limit and job.get_state() != "Done":
                    self.timeline[t]["running"].append("> {} is running".format(job.get_id()))
                    job.run()
                    job.stop()
                    if job.get_state() == "Done":
                        jobs.pop(it)
                    is_selected = True

                it += 1

        self.print_timeline(limit)

    def print_timeline(self, limit):
        """
        A textual overview of what happening during the simulation

        :param limit: the time step limit for the simulator
        """
        jobs = self.sort_all_jobs(limit)

        for job in jobs:

            self.timeline[job.offset]["release"].append(
                "> {} released (deadline = {})".format(job.get_id(), job.deadline))

            if job.deadline <= limit:
                self.timeline[job.deadline]["deadline"].append("> Deadline of {}".format(job.get_id()))

        """for t in range(0, limit + 1):
            print("Instant {}:".format(t))
            for event in self.timeline[t]:
                for e in self.timeline[t][event]:
                    print("\t" + e)"""
