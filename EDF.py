class earliest_deadline_first:
    def __init__(self):
        pass

    def feasibilityIntervalEDF(self, feasibility):
        if feasibility <= 1:
            return True
        else:
            return False  # not schedu