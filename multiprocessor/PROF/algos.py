from abc import ABC, abstractmethod
from typing import List, Optional
from model import Interval, Job, TaskSet


class SchedulingAlgorithm(ABC):
    """Abstract class for any scheduling algorithm"""

    @abstractmethod
    def feasability_interval(self, taskset: TaskSet) -> Interval:
        """Compute the feasibility interval for the given task set"""

    def elect_job(self, jobs: List[Job]) -> Optional[Job]:
        """Decide which job to schedule"""


class EDF(SchedulingAlgorithm):
    """Earliest deadline first"""

    @staticmethod
    def idle_instant(taskset: TaskSet) -> int:
        """Compute the first idle instant of the task set"""
        idle_point = taskset.tasks[-1].worst_case_reponse_time(taskset.tasks[:-1])
        return idle_point

    def feasability_interval(self, taskset: TaskSet) -> Interval:
        if taskset.is_synchronous:
            if taskset.is_constrained:

                return Interval(0, self.idle_instant(taskset))
        raise NotImplementedError("Not yet implemented")

    def elect_job(self, jobs: List[Job]) -> Optional[Job]:
        if len(jobs) == 0:
            return None
        elected = jobs[0]
        for job in jobs:
            if job.deadline < elected.deadline:
                elected = job
        return elected


class RM(SchedulingAlgorithm):
    """Rate Monotinic"""

    def feasability_interval(self, taskset: TaskSet) -> Interval:
        n = len(taskset)
        if taskset.utilisation <= n * (2**(1/n)-1):
            return Interval(0, 0)
        if taskset.is_synchronous:
            if taskset.is_constrained:
                return Interval(0, max(t.deadline for t in taskset.tasks))
        raise NotImplementedError("Not yet implemented")

    def elect_job(self, jobs: List[Job]) -> Optional[Job]:
        if len(jobs) == 0:
            return None
        elected_job = jobs[0]
        for job in jobs:
            if job.task.period < elected_job.task.period:
                elected_job = job
        return elected_job
