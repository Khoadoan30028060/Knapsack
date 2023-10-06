from knapsack import *
import random
import timeit

def generatePopulation(size,items):
	population = []
	genes = [0, 1]
	for _ in range(size):
		chromosome = []
		for _ in range(len(items)):
			chromosome.append(random.choice(genes))
		population.append(chromosome)
	return population

def calculateFitness(Chromosome, Backpack:Knapsack):
    total_weight = 0
    total_value = 0
    check = set()
    for index,value in enumerate(Chromosome):
        if value == 1:
            total_weight += Backpack.items[index].weight
            total_value += Backpack.items[index].value
            check.add(str(Backpack.items[index].classNum))
    if total_weight > Backpack.W:
        return 0
    if len(check) != Backpack.nClass:
        return 0
    return total_value

def Crossover(Parent1, Parent2):
    n = len (Parent1)
    index = random.randint(0, n - 1)
    Child1 = Parent1[0:index] + Parent2[index:]
    Child2 = Parent2[0:index] + Parent1[index:]
    return Child1,Child2

def Mutation(Chromosome):
    index = random.randint(0, len(Chromosome)-1)
    if (Chromosome[index] == 1):
        Chromosome[index] = 0
    else:
        Chromosome[index] = 1
    return Chromosome

def selectionChromosomes (Population,Backpack:Knapsack):
    fitness_values = []
    for Chromosome in Population:
        fitness_values.append(calculateFitness(Chromosome, Backpack))
    total = sum(fitness_values)
    if total != 0:
        fitness_values = [float(i/total) for i in fitness_values]
        Parent1 = random.choices(Population, fitness_values, k=1)[0]
        Parent2 = random.choices(Population, fitness_values, k=1)[0]
        return Parent1, Parent2
    else:
        return -1, -1

def createNextGeneration (Population, Backpack:Knapsack):
    MUTATION_PROBABILITY = 0.1 
    newGen = []
    while (len(newGen) < len(Population)):
        # select two chromosomes
        Parent1,Parent2 = selectionChromosomes(Population, Backpack)
        if Parent1 == -1 or Parent2 == -1:
            break 
        # Crossover
        Child1, Child2 = Crossover(Parent1, Parent2)

        #Mutation
        if random.uniform(0, 1) < MUTATION_PROBABILITY:
            Child1 = Mutation(Child1)
        if random.uniform(0, 1) < MUTATION_PROBABILITY:
            Child2 = Mutation(Child2)
        #add
        # if calculateFitness(Child1,Backpack) != 0:
        #     newGen.append(Child1)
        # if calculateFitness(Child2,Backpack) != 0:
        #     newGen.append(Child2)
        newGen.append(Child1)
        newGen.append(Child2)
    return newGen

def GeneticAlgorithm(Backpack:Knapsack): 
    start_time = timeit.default_timer()
    n = len (Backpack.items)
    Population = generatePopulation(200, Backpack.items)
    best_choice = []
    val = 0
    for i in range(1,1000): # number of generations
        if len(Population) == 0:
            return timeit.default_timer() - start_time, -1, []
        fitness_values = [calculateFitness(Chromosome,Backpack) for Chromosome in Population]
        indexOfBest = fitness_values.index(max(fitness_values))
        if val < fitness_values[indexOfBest]:
            best_choice = Population[indexOfBest]
            val = fitness_values[indexOfBest]
        if i == n * 10: break
        else:
            Population = createNextGeneration(Population, Backpack)
    elapsed_time = timeit.default_timer() - start_time
    return elapsed_time, val, best_choice