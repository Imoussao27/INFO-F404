class tools:
    def __init__(self):
        pass
    def copyList(self, list):
        """
        Copy a list
        :param list: a list of element
        :return: list copy
        """
        copylist = []
        for element in list:
            copylist.append(element)
        return copylist

    def feasibilityInterval(self, WCET, period):
        calcul = 0
        for i in range(len(WCET)):
            calcul += WCET[i] / period[i]
        return calcul
