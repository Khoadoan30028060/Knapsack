class Item:
    def __init__(self, weight=0, value=0, classNum=0) -> None:
        self.weight = weight
        self.value = value
        self.classNum = classNum
    def __str__(self):
        return "(" + str(self.weight) + ", " + str(self.value) + ", " + str(self.classNum) + ')'


class Knapsack:
    def __init__(self, W=0, nClass=0, items=None) -> None:
        if items is None:
            items = []
        self.W = W
        self.nClass = nClass
        self.items = items

    def __str__(self):
        res = ""
        res += "Capacity:" + str(self.W) + '\n'
        res += "There are " + str(self.nClass) + " classes of objects\n\n"
        res += "(weight, value, class label)\n"
        for i in range(len(self.items)):
            res += str(self.items[i]) + '\n'
        return res
