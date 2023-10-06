from knapsack import *
import timeit

def Class_Constraint(item_list: list, problem: Knapsack):
    check_list = [0 for i in range(problem.nClass)]
    for i in range(len(item_list)):
        if item_list[i] == 1:
            check_list[problem.items[i].classNum - 1] = 1
    for i in range(problem.nClass):
        if check_list[i] == 0: return False
    return True

def BruteForce(problem: Knapsack):
    temp_list = [0 for i in range(len(problem.items))]
    bestvalue = -1
    # bestweight = -1
    item_list = []
    start = timeit.default_timer()
    for i in range(pow(2,len(problem.items))):
        j = len(problem.items) - 1 
        tempweight = 0
        tempvalue = 0
        while(temp_list[j] != 0 and j > 0):
            temp_list[j] = 0
            j -= 1
        temp_list[j] = 1
        for k in range(len(problem.items)):
            if (temp_list[k] == 1):
                tempweight += problem.items[k].weight
                tempvalue += problem.items[k].value
        if tempvalue > bestvalue and tempweight <= problem.W and Class_Constraint(temp_list, problem):
            bestvalue = tempvalue
            # bestweight = tempweight
            item_list = list(temp_list)
    end = timeit.default_timer()
    if bestvalue == -1:
        return end - start, -1, []
    else:
        return end - start, bestvalue, item_list
