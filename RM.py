from tools import *
class rate_monotonic:
    def __init__(self):
        self.listRateMonotonic = []
        self.tools = tools()

    def addNewTask(self, listOfTimes, tasks, order):
        """
        Add task in list
        :param listOfTimes: list of deadline of job
        :param tasks: list of task
        :return: a list of task ongoing
        """
        tasksOnGoing = [[] for i in range(len(tasks))]
        for i in range(len(tasks)):
            if (tasks[i] != []):
                tasksOnGoing[i].append(listOfTimes[i])
                tasksOnGoing[i].append(tasks[i][0][0])
                tasksOnGoing[i].append(tasks[i][0][1])
                name = "T" + str(i + 1)
                tasksOnGoing[i].append(name)
                tasksOnGoing[i].append(order.index(name))
        return tasksOnGoing

    def algorithm(self, lcm, WCET, tasks, order):
        listOfTimes = [0 for i in range(len(tasks))]
        countOfJob = self.tools.copyList(WCET)
        time = 0
        tasksOnGoing = self.addNewTask(listOfTimes, tasks, order)  # list of list with period and name of task

        while (len(tasksOnGoing) != 0) and (lcm >= time):  # while there's not task
            onGoing = []
            for index in range(len(tasksOnGoing)):
                if (tasksOnGoing[index] != []):
                    if (tasksOnGoing[index][0] <= time):
                        onGoing.append(tasksOnGoing[index])
                    if (tasksOnGoing[index][1] < time):  # TODO: condition pour verif le missing
                        print("MISSSING")
                        exit(1)

            newTasksOnGoing = []
            for element in tasksOnGoing:
                if element not in onGoing:
                    newTasksOnGoing.append(element)
            tasksOnGoing = newTasksOnGoing

            if (len(onGoing) != 0):
                onGoing.sort(key=lambda a: a[4])  # sort task onGoing #TODO: arranger cette ligne pour les priorités
                job = onGoing[0][3]
                index = int(job[1]) - 1
                tasks[index].remove((int(onGoing[0][1]), int(onGoing[0][2])))
                countOfJob[index] -= 1
                if countOfJob[index] == 0:
                    listOfTimes[index] = int(onGoing[0][1])
                    countOfJob[index] = WCET[index]
                self.listRateMonotonic.append((job, time + 1))
                time += 1
                del onGoing[0]
            else:
                tasksOnGoingEmpty = [[] for i in range(len(tasksOnGoing))]
                if (tasksOnGoing == tasksOnGoingEmpty):
                    break
                else:
                    time += 1
            tasksOnGoing = self.addNewTask(listOfTimes, tasks, order)
        return self.listRateMonotonic
