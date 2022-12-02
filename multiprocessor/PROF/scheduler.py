from typing import List, Optional
from models import Job, TaskSet, Interval
from algos import SchedulingAlgorithm


class Scheduler:
    """Scheduler class"""

    def __init__(self, task_file: str, algo: SchedulingAlgorithm) -> None:
        self.task_set = TaskSet.from_file(task_file)
        self.algo = algo

    def run(self, n_steps: int):
        """Run the scheduler"""
        job_queue = []
        previous_job: Optional[Job] = None
        for t in range(n_steps + 1):
            new_jobs = self.task_set.release_jobs(t)
            job_queue += new_jobs
            elected_job = self.algo.elect_job(job_queue)
            if previous_job is not None and previous_job != elected_job:
                print(previous_job.elected_times[-1], previous_job)
            if elected_job is not None:
                elected_job.schedule(t)
                if elected_job.is_complete:
                    job_queue.remove(elected_job)
            previous_job = elected_job
            missed = self.deadline_misses(job_queue, t)
            if len(missed) > 0:
                print(previous_job.elected_times[-1], previous_job)
                print(f"Deadline missed at t={t} for jobs {missed}")
                return missed, t

    def is_schedulable(self) -> bool:
        """Whether the system is schedulable"""
        return False

    def feasability_interval(self) -> Interval:
        """Compute the feasibility interval"""
        return self.algo.feasability_interval(self.task_set)

    @staticmethod
    def deadline_misses(active_jobs: List[Job], t: int) -> List[Job]:
        """Return the list of jobs that have missed a deadline"""
        missed = []
        for job in active_jobs:
            if t >= job.deadline and job.computation_remaining > 0:
                missed.append(job)
        return missed
