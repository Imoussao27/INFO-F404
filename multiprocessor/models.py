"""Task related classes"""
from dataclasses import dataclass
from typing import ClassVar, Iterable, List, Optional
from math import ceil


@dataclass
class Interval:
    """Interval"""
    start: int
    stop: int

    def __repr__(self) -> str:
        return f"[{self.start:4d}, {self.stop:4d}]"


@dataclass
class Task:
    """A task"""
    num_tasks: ClassVar[int] = 0

    task_id: int
    offset: int
    wcet: int
    deadline: int
    period: int
    jobs_released: int = 0

    def spawn(self, time: int) -> "Job":
        """Spawn a new job"""
        self.jobs_released += 1
        return Job(self, time, self.jobs_released)

    @classmethod
    def from_line(cls, line: str) -> "Task":
        """Create a task from a line in a file"""
        try:
            offset, wcet, deadline, period = line.strip().split()
            cls.num_tasks += 1
            task_id = cls.num_tasks
            return Task(task_id, int(offset), int(wcet), int(deadline), int(period))
        except ValueError:
            print(f"{line} could not be parsed as task")
            exit(0)

    @property
    def is_implicit(self) -> bool:
        """Whether the deadline is implicit"""
        return self.deadline == self.period

    @property
    def is_constrained(self) -> bool:
        """Whether the task has constrained deadlines"""
        return self.deadline <= self.period

    @property
    def utilisation(self) -> float:
        """The task utilisation (wcet/period)"""
        return self.wcet / self.period

    def worst_case_reponse_time(self, higher_priotity_tasks: List["Task"]) -> int:
        """Compute the worst case response time of the task (or the first beyond the deadline)"""
        prev_wk = self.wcet
        wk = self.wcet + sum(ceil(prev_wk/t.period) for t in higher_priotity_tasks)
        while wk != prev_wk and wk < self.deadline:
            prev_wk = wk
            wk = self.wcet + sum(ceil(prev_wk/t.period) * t.wcet for t in higher_priotity_tasks)
        return wk


@dataclass
class Job:
    """A Job is an instance of a class"""
    task: Task
    release_time: int
    deadline: int
    job_id: int
    computation_remaining: int
    elected_times: List[Interval]

    def __init__(self, related_task: Task, release_time: int, job_id: int) -> None:
        self.task = related_task
        self.release_time = release_time
        self.deadline = self.release_time + self.task.deadline
        self.computation_remaining = self.task.wcet
        self.elected_times = []
        self.job_id = job_id

    def schedule(self, t: int):
        """Schedule the task at time t"""
        self.computation_remaining -= 1
        if len(self.elected_times) == 0:
            self.elected_times.append(Interval(t, t+1))
        else:
            last_elected = self.elected_times[-1]
            if last_elected.stop == t:
                last_elected.stop = t + 1
            else:
                self.elected_times.append(Interval(t, t + 1))

    @property
    def is_complete(self) -> bool:
        """Whether the job is complete"""
        return self.computation_remaining <= 0

    @property
    def completion_time(self) -> Optional[int]:
        """Completion time of the task (or None if not completed)"""
        if not self.is_complete:
            return None
        return self.elected_times[-1].stop

    def __repr__(self) -> str:
        return f"T{self.task.task_id}J{self.job_id}"


@dataclass
class TaskSet:
    """A task set"""
    tasks: List[Task]

    @property
    def is_implicit(self) -> bool:
        """Whether the task set has implicit deadlines"""
        return all(t.is_implicit for t in self.tasks)

    @property
    def is_constrained(self) -> bool:
        """Whether the task set has constrained deadlines"""
        return all(t.is_constrained for t in self.tasks)

    @property
    def is_synchronous(self) -> bool:
        """Whether the task set is synchronous"""
        offset = self.tasks[0].offset
        return all(t.offset == offset for t in self.tasks)

    @property
    def utilisation(self) -> float:
        """The task set utilisation (sum of task utilisations)"""
        return sum(t.utilisation for t in self.tasks)

    @staticmethod
    def from_file(filename: str) -> "TaskSet":
        """Read the tasks set from a file"""
        with open(filename, "r", encoding="utf8") as f:
            lines = f.readlines()
            tasks = [Task.from_line(line) for line in lines]
            return TaskSet(tasks)

    def release_jobs(self, t: int) -> List[Job]:
        """Release new jobs for each concerned task"""
        jobs = []
        for task in self.tasks:
            if t % task.period == 0:
                jobs.append(task.spawn(t))
        return jobs

    def __iter__(self) -> Iterable[Task]:
        return iter(self.tasks)

    def __len__(self) -> int:
        return len(self.tasks)
