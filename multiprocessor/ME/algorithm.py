

class schedule:
    def run(self, tasks, feasibility):
        #ongoingTasksList.sort(key=lambda x: x.wcet)
        time = 0
        ongoingTask = []

    def getOngoingTask(self, tasks, time):
        ongoingTask = []
        for task in tasks:
            if not task.isDone:
                pass


    def create(self, tasks, feasability):
        newTasksList = []
        for task in tasks:
            sousTasksList = []
            newOffset = task.offset
            deadline = task.deadline
            numberOfJob = round(feasability/deadline)
            for i in range(1, numberOfJob+1):
                for j in range(task.wcet):
                    calcul = deadline * i
                    sousTask = task.sousTask(newOffset, calcul)
                    sousTasksList.append(sousTask)
                newOffset = deadline * i
            newTasksList.append(sousTasksList)
        return newTasksList




