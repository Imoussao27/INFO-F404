import Task as task

def readFile(nameFile):
    file = open(nameFile, "r")
    textFile = file.readlines()
    tasksList = []

    for line in textFile:
        linelist = line.split(" ")
        newTask = task.Task(0, linelist[0], linelist[1], linelist[2], linelist[3].strip())
        tasksList.append(newTask)


readFile("test")
