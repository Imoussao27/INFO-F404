from Parser import *
from Partitioner import *

if __name__ == '__main__':
    parser = Parser()
    heuristic, sort, limit, cores_number = parser.get_options()
    tasks = parser.get_tasks()  #une liste de task de type task
    partitioner = Partitioner(tasks, heuristic, sort, limit, cores_number) #genre limit = 400
    partitioner.run()

    if partitioner.is_partitioned():
        for core in partitioner.get_cores():
            print(core)
            core.schedule(limit)
    else:
        print("Cannot be partitioned")
