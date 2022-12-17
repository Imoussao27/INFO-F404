#! /usr/bin/env python3
from schedulers import Scheduler
from algos import RM, EDF

if __name__ == "__main__":
    algo = RM()
    scheduler = Scheduler("test", algo)
    fi = scheduler.feasability_interval()
    print(fi)
    scheduler.run(fi.stop)
