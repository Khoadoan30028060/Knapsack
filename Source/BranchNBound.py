from knapsack import *
import timeit


def getRatio(item: Item):
    return item.value / item.weight


class KnapsackNode:
    def __init__(self, itemsList: list, totalWeight, totalValue, classSet: set, level = 0, bound = 0) -> None:
        self.itemsList = itemsList # list of chosen items
        self.totalWeight = totalWeight
        self.totalValue = totalValue
        self.classSet = classSet # set of chosen class (unique)
        self.level = level 
        self.bound = bound 
    
    def getBound(self, problem: Knapsack):
        rWeight = problem.W - self.totalWeight
        self.bound = self.totalValue
        for i in range(self.level + 1, len(problem.items)): # loop through every remaining items
            kItem = problem.items[i]
            if rWeight >= kItem.weight:
                self.bound += kItem.value
                rWeight -= kItem.weight
            else:
                self.bound += rWeight * getRatio(kItem)
                break
        return self.bound
    
    def isPromising(self, problem: Knapsack, best_value):
        return (self.totalWeight <= problem.W 
                and self.bound > best_value)
    


def BranchAndBound(problem: Knapsack):
    beforeSort = problem.items.copy()

    start = timeit.default_timer()
    problem.items.sort(reverse=True, key=getRatio)
    myStack = [KnapsackNode([], 0, 0, set(), -1, 0)] # put an empty node with level starts from -1
    sol = None
    best_value = -1
    
    promisingLeft = False
    promisingRight = False
    while len(myStack) != 0:
        u = myStack.pop()
        
        if (u.level != len(problem.items) - 1): # if u is not a leaf node
            curItem = problem.items[u.level + 1]
            
            # create a child with new item
            newSet = u.classSet.copy()
            newSet.add(curItem.classNum)
            childWithItem = KnapsackNode(u.itemsList + [curItem],
                                         u.totalWeight + curItem.weight,
                                         u.totalValue + curItem.value,
                                         newSet,
                                         u.level + 1)
            childWithItem.getBound(problem)
            
            if childWithItem.isPromising(problem, best_value):
                promisingLeft = True
                if childWithItem.totalValue > best_value and len(childWithItem.classSet) == problem.nClass:
                    best_value = childWithItem.totalValue
                    sol = childWithItem.itemsList
            else:
                promisingLeft = False
            # create a child without new item
            # level + 1: to prevent inf loop (the child node has difference level from its parent)
            # to make the algorithm possible to terminate at the first if condition 
            childWithoutItem = KnapsackNode(u.itemsList,
                                            u.totalWeight,
                                            u.totalValue,
                                            u.classSet,
                                            u.level + 1)
            childWithoutItem.getBound(problem)
            if childWithoutItem.isPromising(problem, best_value):
                promisingRight = True
                if childWithoutItem.totalValue > best_value and len(childWithoutItem.classSet) == problem.nClass:
                    best_value = childWithoutItem.totalValue
                    sol = childWithoutItem.itemsList
            else:
                promisingRight = False
            
            if promisingRight:
                myStack.append(childWithoutItem)
            if promisingLeft:
                myStack.append(childWithItem)
            
    end = timeit.default_timer()
    
    if sol: # solution found
        chosenItems = [0] * len(problem.items)
        for i in range(len(beforeSort)):
            problem.items[i] = beforeSort[i]
            if problem.items[i] in sol:
                chosenItems[i] = 1
        return end - start, best_value, chosenItems
    else: # no solution found
        return end - start, -1, []
