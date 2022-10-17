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
                isWCET = False; 
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


def rateMonotonic():
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



def main():
    lists = readFile("taskset1") # order priority 
    print(lists)
    lcm = findLeastCommonMultiple(sorted(lists[1])) #Find the best lcm 
    listPeriodOfTasks = periodOfTasks(lcm, lists[1])

    print(listPeriodOfTasks)

    example = [('T1', 20), ('T2', 5), ('T3', 10)]
    example.sort(key=lambda a: a[1])
    print(example)

    exo = [('T1', 20), ('T2', 5), ('T3', 10)]
    exo.sort(key=lambda a: a[1])
    print(exo)


if __name__ == '__main__':
    main()