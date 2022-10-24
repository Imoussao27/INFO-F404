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


def leastCommonMultiple(number1, number2):
    """
    Apply the least common multiple on two number
    :param number1: integer represent a period
    :param number2: integer represent a period
    :return: number of least common multiple
    """
    if (number1 > number2):  # Find the greater number
        greaterNumber = number1
    else:
        greaterNumber = number2

    isFindLCM = True
    while (isFindLCM):  # calcul lcm
        if ((greaterNumber % number1 == 0) and (greaterNumber % number2 == 0)):
            lcm = greaterNumber
            isFindLCM = False
        greaterNumber += 1
    return lcm


def findLeastCommonMultiple(period):
    """
    Find the greater least common multiple
    :param period: list of number of period
    :return: integer of the greater common multiple
    """
    lcm = leastCommonMultiple(period[0], period[1])
    for i in range(1, len(period) - 1):
        find_lcm = leastCommonMultiple(period[i], period[i + 1])
        if lcm <= find_lcm:
            lcm = find_lcm
    return lcm


def priority(period):
    pass


def earliestDeadLineFirst():
    pass


def periodOfTasks(lcm, WCET, period):
    """

    :param lcm: number of lcm
    :param period: list of number of period
    :return:
    """
    listPeriodOfTasks = []
    listWCETOfTasks = []
    for element in period:
        listJob = []
        listJobWCET = []
        numberOfJob = round(lcm / element)
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


def copyList(list):
    """
    Copy a list
    :param list: a list of element
    :return: list copy
    """
    copylist = []
    for element in list:
        copylist.append(element)
    return copylist


def rateMonotonic(WCET, tasks):
    """
    Function apply algo of rate monotonic
    :param WCET: list of number of WCET
    :param tasks: list of task and his jobs
    :return: list with task, job and their time
    """
    listRateMonotonic = []
    listOfTimes = [0 for i in range(len(tasks))]
    countOfJob = copyList(WCET)
    time = 0
    tasksOnGoing = addNewTask(listOfTimes, tasks)  # list of list with period and name of task

    while (len(tasksOnGoing) != 0):  # while there's not task
        onGoing = []
        for index in range(len(tasksOnGoing)):
            if (tasksOnGoing[index] != []):
                if (tasksOnGoing[index][0] <= time):
                    onGoing.append(tasksOnGoing[index])

        newTasksOnGoing = []
        for element in tasksOnGoing:
            if element not in onGoing:
                newTasksOnGoing.append(element)
        tasksOnGoing = newTasksOnGoing

        if (len(onGoing) != 0):
            onGoing.sort(key=lambda a: a[1]) #sort task onGoing
            job = onGoing[0][3]
            index = int(job[1]) - 1
            tasks[index].remove((int(onGoing[0][1]), int(onGoing[0][2])))
            countOfJob[index] -= 1
            if countOfJob[index] == 0:
                listOfTimes[index] = int(onGoing[0][1])
                countOfJob[index] = WCET[index]
            listRateMonotonic.append((job, time + 1))
            time += 1
            del onGoing[0]
        else:
            tasksOnGoingEmpty = [[] for i in range(len(tasksOnGoing))]
            if (tasksOnGoing == tasksOnGoingEmpty):
                break
            else:
                time += 1
        tasksOnGoing = addNewTask(listOfTimes, tasks)
    return listRateMonotonic


def addNewTask(listOfTimes, tasks):
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
            tasksOnGoing[i].append("T" + str(i + 1))
    return tasksOnGoing


def toPrint(listeUniprocessor):
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
            time = listeUniprocessor[index - 1][1]
            count = 1
    listToPrint.append([listeUniprocessor[-1][0], stock, count + stock])
    return listToPrint


def sortListToPrint(listToPrint, listWCETOfTasks):
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

def feasibilityInterval(WCET, period):
    calcul = 0
    for i in range(len(WCET)):
        calcul += WCET[i] / period[i]
    return calcul

def feasibilityIntervalRM(feasibility):
    #call the good function
    if(feasibility <= 0.69):
        pass
    elif (feasibility <= 0.69 and feasibility <= 1):
        pass
    else:
        pass

def feasibilityIntervalEDF(feasibility):
    if feasibility <= 1:
        return True
    else:
        return False #not schedu

def display(listToPrint):
    for element in listToPrint:
        taskJob = element[0] + element[3]
        print([element[1], element[2]], taskJob)

def main():
    lists = readFile("taskset1")  # order priority
    lcm = findLeastCommonMultiple(sorted(lists[1]))  # Find the best lcm
    listsTasks = periodOfTasks(lcm, lists[0], lists[1])
    listPeriodOfTasks = listsTasks[0]
    listWCETOfTasks = listsTasks[1]
    listNumberOfTasks = numberOfTasks(lists[0], listPeriodOfTasks)
    listRateMonotonic = rateMonotonic(lists[0], listNumberOfTasks)
    listToPrint = toPrint(listRateMonotonic)
    sortedListToPrint = sortListToPrint(listToPrint, listWCETOfTasks)
    #display(sortedListToPrint)
    print(feasibilityInterval(lists[0], lists[1]))


if __name__ == '__main__':
    main()
