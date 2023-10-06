from types import new_class
from knapsack import *
import random
import timeit
import math

def fitness(knap: Knapsack, individual): # returns sum of values
    if individual is None:
        return 0
    sum_w = 0
    sum_v = 0
    checkClass = list(0 for _ in range(knap.nClass))
    for i in range (len(individual)):
        if individual[i] == 1:
            sum_w += knap.items[i].weight
            sum_v += knap.items[i].value
            checkClass[knap.items[i].classNum - 1] += 1
    if (sum_w > knap.W) or (0 in checkClass):
        return 0
    return sum_v

def createIndividual(n): # generate an individual
    return [random.randint(0, 1) for _ in range(n)]

def selectBestIndivi(population, knap: Knapsack, beamWidth):
    fitnessList = [fitness(knap, indi) for indi in population]
    sortedList = [x for _, x in sorted(zip(fitnessList, population), reverse=True)]
    return sortedList[:beamWidth]

def createPopulationNearby(populationSize, currIndivi, numItem): # Random a new list of indi base on good indi list
    newList = []
    i = 0
    while i < populationSize and i < len(currIndivi):
        temp = list(currIndivi[i])
        newList.append(temp)
        numGen = random.randint(int(numItem / 3), int(numItem / 2))
        for _ in range (numGen):
            pos = random.randint(0, numItem - 1)
            temp[pos] = 1 - temp[pos]
            newList.append(temp.copy())
        i += 1
    return newList

def localBeamSearch(knap: Knapsack, numIteration, populationSize, beamWidth):
    numItem = len(knap.items)
    population = [createIndividual(numItem) for _ in range(populationSize)] # init individuals
    bestIndivi = None
    for _ in range(numIteration):
        currIndivi = selectBestIndivi(population, knap, beamWidth)
        try:
            fitnessOfCurr_0 = fitness(knap, currIndivi[0])
        except:
            continue
        if fitnessOfCurr_0 != 0:
            if bestIndivi is None or (fitness(knap, bestIndivi) < fitnessOfCurr_0):
                bestIndivi = currIndivi[0].copy()
        population = createPopulationNearby(populationSize, currIndivi, numItem)
    return bestIndivi

def LocalBeamSearch(knap: Knapsack):
    if (len(knap.items) <= 30):
        pop_size = int(len(knap.items))
        beam_width = math.ceil(pop_size / 2)
        num_iter = 7000
    elif (len(knap.items) <= 50):
        pop_size = int(len(knap.items) / 2)
        beam_width = int(pop_size)
        num_iter = 10000
    elif (len(knap.items) <= 300):
        pop_size = int(len(knap.items) / 4)
        beam_width = int(pop_size)
        num_iter = 10000
    elif (len(knap.items) < 450):
        pop_size = int(len(knap.items) / 10)
        beam_width = int(pop_size / 2)
        num_iter = 10000
    else:
        pop_size = int(len(knap.items) / 100)
        beam_width = int(pop_size / 2)
        num_iter = 10000
    

    start = timeit.default_timer()
    final = localBeamSearch(knap, num_iter, pop_size, beam_width)
    stop = timeit.default_timer()
    f = fitness(knap, final)
    if final: # solution found
        return stop - start, f, final
    else:
        return stop - start, -1, []