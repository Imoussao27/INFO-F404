def readFile(nameFile): # read file taskset 
    WCET = []
    period = []
    tasks = []

    file = open(nameFile, "r") 
    tasks = file.readlines()

    count = 1
    for line in tasks:
        isWCET = True 
        for word in line.split(" "): #split white-spaces
            word = int(word.strip('\n')) #convert string to int
            if(isWCET):
                WCET.append(word)
                isWCET = False
            else:
                period.append(word)

    return WCET, period


def leastCommonMultiple(number1, number2):
    if(number1 > number2): #Find the greater number 
        greaterNumber = number1
    else:
        greaterNumber = number2

    isFindLCM = True
    while(isFindLCM): #calcul lcm
       if((greaterNumber % number1 == 0) and (greaterNumber % number2 == 0)):
           lcm = greaterNumber
           isFindLCM = False
       greaterNumber += 1
    return lcm

def findLeastCommonMultiple(period):
    lcm = leastCommonMultiple(period[0], period[1])
    for i in range(1, len(period)-1):
        find_lcm = leastCommonMultiple(period[i], period[i+1])
        if lcm <= find_lcm:
            lcm = find_lcm
    return lcm

def priority(period):
    pass

def earliestDeadLineFirst():
    pass 

def periodOfTasks(lcm, period):
    listPeriodOfTasks = []
    for element in period:
        listJob = []
        numberOfJob = round(lcm / element)
        for i in range(1, numberOfJob+1):
            calcul = element * i
            listJob.append(calcul)
        listPeriodOfTasks.append(listJob)
    return listPeriodOfTasks

def numberOfTasks(WCET, liste):
    newListe = []
    for i in range(len(liste)):
        miniListe = []
        for line in liste[i]:
            for j in range(WCET[i]):
                miniListe.append((line, 1))
        newListe.append(miniListe)
    return newListe

def rateMonotonic(WCET, tasks):
    listRateMonotonic = []
    listOfTimes = [0, 0, 0]
    countOfJob = [3, 2, 2]
    tasksOnGoing = [[] for i in range(3)]

    time = 0
    if(time == 0):
        for i in range(len(tasks)):
            tasksOnGoing[i].append(time)
            tasksOnGoing[i].append(tasks[i][0][0])
            tasksOnGoing[i].append(tasks[i][0][1])
            tasksOnGoing[i].append("T" + str(i+1))


    while(len(tasksOnGoing) != 0):
        onGoing = []
        print("tasksOnGoing =", tasksOnGoing)
        for index in range(len(tasksOnGoing)):
            if(tasksOnGoing[index]!=[]):
                if(tasksOnGoing[index][0] <= time):
                    onGoing.append(tasksOnGoing[index])

        newTasksOnGoing = []
        for element in tasksOnGoing:
           if element not in onGoing:
            newTasksOnGoing.append(element)
        tasksOnGoing = newTasksOnGoing
        print("OnGoing = ", onGoing)

        if(len(onGoing) != 0):
            onGoing.sort(key=lambda a: a[1])
            job = onGoing[0][3]
            index = int(job[1]) - 1
            #print("tasks == ", tasks)
            #print((int(onGoing[0][1]), int(onGoing[0][2])))
            tasks[index].remove((int(onGoing[0][1]), int(onGoing[0][2])))
            countOfJob[index] -= 1 
            if(countOfJob[index] == 0):
                listOfTimes[index] = int(onGoing[0][1])
                countOfJob[index] = WCET[index]
            #print("tasks == ", tasks)
            listRateMonotonic.append(job)
            time += 1
            del onGoing[0]
            #print(listRateMonotonic)
        else:
            break
        
        #print(listOfTimes, " is the list of times")
        print(listRateMonotonic)
        print(addNewTask(listOfTimes, tasks))
        print("-----------------------------------------------------")
        tasksOnGoing = addNewTask(listOfTimes, tasks)

def addNewTask(listOfTimes, tasks):
    tasksOnGoing = [[] for i in range(3)]
    for i in range(len(tasks)):
        if(tasks[i] != []):
            tasksOnGoing[i].append(listOfTimes[i])
            tasksOnGoing[i].append(tasks[i][0][0])
            tasksOnGoing[i].append(tasks[i][0][1])
            tasksOnGoing[i].append("T" + str(i+1))

    return tasksOnGoing


def main():
    lists = readFile("taskset1") # order priority 
    lcm = findLeastCommonMultiple(sorted(lists[1])) #Find the best lcm 
    listPeriodOfTasks = periodOfTasks(lcm, lists[1])
    listNumberOfTasks = numberOfTasks(lists[0], listPeriodOfTasks)
    print(rateMonotonic(lists[0], listNumberOfTasks))
    


    example = [('T1', 20), ('T2', 5), ('T3', 10)]
    example.sort(key=lambda a: a[1])


if __name__ == '__main__':
    main()