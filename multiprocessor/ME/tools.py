from math import gcd

class tools:
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

    def leastCommonMultiple(self, period):
        """
        Function calculate least common multiple
        :param period: list of period
        :return: int LCM
        """
        lcm = 1
        for elem in period:
            lcm = lcm * elem // gcd(lcm, elem)
        return lcm

    def feasibilityInterval(self, WCET, period):
        """
        Function to calcul feasibility interval
        :param WCET: list of WCET
        :param period: list of period
        :return: feasibility interval
        """
        calcul = 0
        for i in range(len(WCET)):
            calcul += WCET[i] / period[i]
        return calcul
