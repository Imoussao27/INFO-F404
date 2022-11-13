from rm import *
from edf import*

def readFile(nameFile):  # read file taskset
    """
    Read a file and return his contents in two lists
    :param nameFile: string name of file
    :return: two lists of numbers
    """
    WCET = []
    period = []

    file = open(nameFile, "r")
    tasks = file.readlines()

    for line in tasks:
        isWCET = True
        for word in line.split(" "):  # split white-spaces
            word = int(word.strip('\n'))  # convert string to int
            if (isWCET):
                WCET.append(word)
                isWCET = False
            else:
                period.append(word)
    return WCET, period

def periodOfTasks(maxTask, WCET, period):
    """
    :param maxTask: max deadline
    :param period: list of number of period
    :return:
    """
    listPeriodOfTasks = []
    listWCETOfTasks = []
    for element in period:
        listJob = []
        listJobWCET = []
        numberOfJob = round(maxTask / element)
        for i in range(1, numberOfJob + 1):
            calcul = element * i
            listJob.append(calcul)
            listJobWCET.append(WCET[period.index(element)])
        listPeriodOfTasks.append(listJob)
        listWCETOfTasks.append(listJobWCET)
    return listPeriodOfTasks, listWCETOfTasks


def numberOfTasks(WCET, liste):
    """
    create a list of list with the number WCET for the period
    :param WCET: list of WCET
    :param liste: a list with job deadline
    :return: a list of list with the number WCET for the period
    """
    newListe = []
    for i in range(len(liste)):
        miniListe = []
        for line in liste[i]:
            for j in range(WCET[i]):
                miniListe.append((line, 1))
        newListe.append(miniListe)
    return newListe

def tasksWithTimes(listeUniprocessor):
    time = 0
    count = 1
    stock = 0
    listToPrint = []
    for index in range(1, len(listeUniprocessor)):
        if (listeUniprocessor[index - 1][0] == listeUniprocessor[index][0]):
            count += 1
        else:
            stock = listeUniprocessor[index][1] - 1
            listToPrint.append([listeUniprocessor[index - 1][0], time, count + time])
            time = listeUniprocessor[index][1] - 1
            count = 1
    listToPrint.append([listeUniprocessor[-1][0], stock, count + stock])
    return listToPrint


def addJobOnTask(listToPrint, listWCETOfTasks):
    for element in listToPrint:
        calcul = element[2] - element[1]
        index = int(element[0][1]) - 1
        for i in range(len(listWCETOfTasks[index])):
            if (listWCETOfTasks[index][i] != 0):
                value = listWCETOfTasks[index][i]
                newValue = value - calcul
                if (newValue == 0):
                    listWCETOfTasks[index][i] = 0
                    element.append("J" + str(i + 1))
                    break
                elif (newValue > 0):
                    listWCETOfTasks[index][i] = newValue
                    element.append("J" + str(i + 1))
                    break
                else:
                    element.append("J" + str(i + 1))
                    listWCETOfTasks[index][i] = 0
                    calcul = - newValue
    return listToPrint

def display(algo, listToPrint):
    listToVisual = [[] for i in range(4)] #TODO: changer ça
    if not algo.isSchedule:
        algo.deadlineMiss = listToPrint[-1][0] + listToPrint[-1][-1]
        del listToPrint[-1]
    for element in listToPrint:
        taskJob = element[0] + element[3]
        index = int(element[0][1]) - 1
        listToVisual[index].append((element[1], element[2] - element[1]))
        print([element[1], element[2]], taskJob)
    return listToVisual

def priorityTask(lists):
    """
    Add name of tasks
    :param lists: list of priority task
    :return: list of priority task with their name
    """
    for i in range(len(lists)):
        name = "T"
        lists[i].append(name+str(i+1))

def orderPriority(period):
    """
    Function to handle the priority of task to RM
    :param period: list of period
    :return: list with the task priority
    """
    tool = tools()
    orderPeriod = sorted(tool.copyList(period))
    orderTask = []
    nameTask = []
    for i in range(len(period)):
        for j in range(len(orderPeriod)):
            if orderPeriod[i] == period[j]:
                name = "T"+str(j+1)
                if j not in nameTask:
                    orderTask.append(name)
                    nameTask.append(j)
                    break
    return orderTask


def runAlgorithm(algorithm, WCET, period, listsTasks):
    """
    Run algorithm RM or EDF
    :param algorithm: name of algorithm
    :param WCET: list of number of WCET
    :param period: list of number of period
    :param listsTasks: list of tasks
    :return: list of jobs with task
    """
    listOrderPriority = orderPriority(period)
    listNumberOfTasks = numberOfTasks(WCET, listsTasks[0])
    listRateMonotonic = algorithm.run(listNumberOfTasks, listOrderPriority)
    listToPrint = tasksWithTimes(listRateMonotonic)
    sortedListToPrint = addJobOnTask(listToPrint, listsTasks[1])
    return display(algorithm, sortedListToPrint)


def main():
    nameFile = "taskset1" # sys.argv[2]
    nameAlgo = "edf"  #sys.argv[1].lower()
    if nameAlgo == "rm" or nameAlgo == "edf":
        print("Running with " + nameAlgo.upper())
        lists = readFile(nameFile)  # order priority
        maxTask = tools().leastCommonMultiple(lists[1])
        if nameAlgo == "rm":
            algo = rate_monotonic(lists[0], lists[1]) #rate_monotonic(lists[0], lists[1])
        else:
            algo = earliest_deadline_first(lists[0], lists[1]) #earliest_deadline_first(lists[0], lists[1])
        listsTasks = periodOfTasks(maxTask, lists[0], lists[1])
        listAllTasks = runAlgorithm(algo, lists[0], lists[1], listsTasks)
        algo.visualization(listAllTasks, nameFile, nameAlgo)
        if algo.isSchedule:
            print("The system is schedulable!")
        else:
            print("The system is not schedulable because deadline miss for", algo.deadlineMiss, "!")
            exit(1)
    else:
        print("You have to write rm OR edf.")
        print("Don't to write the name of the file.")
        exit(1)

if __name__ == '__main__':
    main()