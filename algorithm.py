import matplotlib.pyplot as plt
from tools import *
from math import *
class algorithm:
    def __init__(self, WCET, period):
        self.listRateMonotonic = []
        self.tool = tools()
        self.WCET = WCET
        self.period = period
        self.isSchedule = True

    def getFeasibility(self):
        return self.tool.feasibilityInterval(self.WCET, self.period)

    def setIsFeasibility(self, isFeasibility):
        self.isSchedule = isFeasibility

    def run(self, lcm, tasks, order, numberOrder):
        print("Feasibility interval is [ 0,", lcm,"]")
        return self.algorithm(lcm, tasks, order, numberOrder)

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

    def algorithm(self, lcm, tasks, order, numberOrder):
        listOfTimes = [0 for i in range(len(tasks))]
        countOfJob = self.tool.copyList(self.WCET)
        time = 0
        tasksOnGoing = self.addNewTask(listOfTimes, tasks, order)  # list of list with period and name of task

        while (len(tasksOnGoing) != 0) and (lcm >= time):  # while there's not task
            onGoing = []
            for index in range(len(tasksOnGoing)):
                if (tasksOnGoing[index] != []):
                    if (tasksOnGoing[index][0] <= time):
                        onGoing.append(tasksOnGoing[index])

                    if (tasksOnGoing[index][1] <= time):
                        return self.listRateMonotonic

            newTasksOnGoing = []
            for element in tasksOnGoing:
                if element not in onGoing:
                    newTasksOnGoing.append(element)
            tasksOnGoing = newTasksOnGoing

            if (len(onGoing) != 0):
                onGoing.sort(key=lambda a: a[numberOrder])  # sort task by priority onGoing
                job = onGoing[0][3]
                index = int(job[1]) - 1
                tasks[index].remove((int(onGoing[0][1]), int(onGoing[0][2])))
                countOfJob[index] -= 1
                if countOfJob[index] == 0:
                    listOfTimes[index] = int(onGoing[0][1])
                    countOfJob[index] = self.WCET[index]
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

    def getSchedule(self):
        return self.isSchedule

    def visualizationTool(self, lcm):
        # Declaring a figure "gnt"
        fig, gnt = plt.subplots()

        # Setting Y-axis limits
        gnt.set_ylim(0, 50)

        # Setting X-axis limits
        gnt.set_xlim(0, lcm)

        # Setting labels for x-axis and y-axis
        gnt.set_xlabel('seconds since start')
        gnt.set_ylabel('Processor')

        # Setting ticks on y-axis
        gnt.set_yticks([15, 25, 35])
        # Labelling tickes of y-axis
        gnt.set_yticklabels(['1', '2', '3'])

        # Setting graph attribute
        gnt.grid(True)

        # Declaring a bar in schedule
        gnt.broken_barh([(40, 50)], (30, 9), facecolors=('tab:orange'))

        # Declaring multiple bars in at same level and same width
        gnt.broken_barh([(110, 10), (150, 10)], (10, 9),
                        facecolors='tab:blue')

        gnt.broken_barh([(10, 50), (100, 20), (130, 10)], (20, 9),
                        facecolors=('tab:red'))

        plt.savefig("gantt1.png")