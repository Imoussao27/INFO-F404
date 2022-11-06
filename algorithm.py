import matplotlib.pyplot as plt
from tools import *

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
        """
        Algorithm to schedule the tasks
        :param lcm: least common multiple
        :param tasks: list of task
        :param order: priority of job
        :param numberOrder: number to order list
        :return: list with tasks scheduled
        """
        listOfTimes = [0 for i in range(len(tasks))]
        countOfJob = self.tool.copyList(self.WCET) #copy of WCET
        time = 0
        tasksOnGoing = self.addNewTask(listOfTimes, tasks, order)  # list of list with period and name of task

        while (len(tasksOnGoing) != 0) and (lcm >= time):  # while there's not task
            onGoing = []
            for index in range(len(tasksOnGoing)):
                if (tasksOnGoing[index] != []):
                    if (tasksOnGoing[index][0] <= time):
                        onGoing.append(tasksOnGoing[index])

                    if (tasksOnGoing[index][1] <= time): #verify if there is missing task
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
                if (tasksOnGoing == tasksOnGoingEmpty): #verify if there is task yet
                    break
                else:
                    time += 1
            tasksOnGoing = self.addNewTask(listOfTimes, tasks, order) #add the next tasks
        return self.listRateMonotonic

    def getSchedule(self):
        return self.isSchedule

    def visualizationTool(self, lcm, listAllTasks, size,numberOfTask, name):
        """
         Function to create a graphical to visual the representation of the execution
        :param lcm: least common multiple
        :param listAllTasks: list of all task with job
        :param numberOfTask: number of tasks
        :param name: name of file
        :return: None
        """
        # Setting
        fig, gnt = plt.subplots()
        gnt.set_xlabel('Time')
        gnt.grid(True)

        gnt.set_ylim(0, numberOfTask*10)
        gnt.set_xlim(0, lcm)

        # Setting ticks
        listSetyTicklabels, listSetyTicks = self.settingTicks(size)

        gnt.set_yticks(listSetyTicks)
        gnt.set_yticklabels(listSetyTicklabels)

        # Declaring a bar in schedule
        count = 0
        for element in listAllTasks:
            gnt.broken_barh(element, (count, 10), facecolors=('tab:blue'))
            count += 10

        plt.savefig(name + ".png")

    def settingTicks(self, size):
        """
        Function to handle setting ticks
        :param size: number of tasks
        :return: set of ticks and name of tasks
        """
        listSetyTicks = []
        listSetyTicklabels = []
        for i in range(size):
            listSetyTicks.append((i + 1) * 10)
            listSetyTicklabels.append('Task' + str(i + 1))
        return listSetyTicklabels, listSetyTicks