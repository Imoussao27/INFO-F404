import Task as task
import algorithm as algo

def readFile(nameFile):
    file = open(nameFile, "r")
    textFile = file.readlines()
    tasksList = []
    id = 1
    for line in textFile:
        linelist = line.split(" ")
        newTask = task.Task(id, int(linelist[0]), int(linelist[1]), int(linelist[2]), int(linelist[3].strip()))
        tasksList.append(newTask)
        id += 1

    return tasksList

def main():
    tasksList = readFile("test")
    newtasks = algo.schedule().create(tasksList, 12)
    #ongoingTasksList = algo.algorithm().schedulerAlgo(tasksList)
    for element in newtasks:
        for task in element:
            task.ToString()
        print("----------------------------")

main()
