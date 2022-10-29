from RM import *
from tools import *
from math import *

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
            time = listeUniprocessor[index + 1][1] - 2
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

def display(listToPrint):
    for element in listToPrint:
        taskJob = element[0] + element[3]
        print([element[1], element[2]], taskJob)

def priorityTask(lists):
    for i in range(len(lists)):
        name = "T"
        lists[i].append(name+str(i+1))

def orderPriority(period):
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


def runAlgorithm(algorithm, WCET, period, lcm, listsTasks):
    listOrderPriority = orderPriority(period)
    listNumberOfTasks = numberOfTasks(WCET, listsTasks[0])
    listRateMonotonic = algorithm.run(lcm, listNumberOfTasks, listOrderPriority)
    listToPrint = tasksWithTimes(listRateMonotonic)
    sortedListToPrint = addJobOnTask(listToPrint, listsTasks[1])
    display(sortedListToPrint)


def main():
    isRate = True
    lists = readFile("taskset1")  # order priority
    if(isRate):
        lcm = findLeastCommonMultiple(sorted(lists[1]))  # Find the best lcm
        listsTasks = periodOfTasks(lcm, lists[0], lists[1])
        runAlgorithm(rate_monotonic(lists[0], lists[1]), lists[0], lists[1], lcm, listsTasks)



if __name__ == '__main__':
    main()