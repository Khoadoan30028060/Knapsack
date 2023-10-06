import os
from BranchNBound import *
from BruteForce import *
from GeneticAlgorithm import *
from LocalBeamSearch import *

def readInput(filename=""):
    ifs = open(filename, 'r')

    W = float(ifs.readline())
    n = int(ifs.readline())
    packBack = Knapsack(W, n)
    weights = ifs.readline().split(', ')
    values = ifs.readline().split(', ')
    classNum = ifs.readline().split(', ')
    for i in range(len(weights)):
        item = Item(float(weights[i]), int(values[i]), int(classNum[i]))
        packBack.items.append(item)

    ifs.close()
    return packBack

def writeOutput(filename, value, solution):
    ofs = open(filename, 'w')
    if value != -1:
        ofs.write(str(value) + '\n')
    else:
        ofs.write(str(0) + '\n')
    ofs.write(', '.join(str(el) for el in solution))
    ofs.close()

if __name__ == '__main__':
    while True:
        os.system("cls")
        print("\n ************Algorithm************")
        print("*       1.   Brute Force          *")
        print("*       2. Branch and Bound       *")
        print("*       3. Local Beam Search      *")
        print("*       4. Genetic Algorithm      *")
        print("*       0.       Exit             *")
        print(" *********************************\n")
        algo = -1
        while algo < 0 or algo > 4:
            algo = int(input("Choose an algorithm to run: "))
        if algo == 0:
            print("Goodbye")
            break
        print("Input format: INPUT_x with x is the sequence")
        while True:
            st = int(input("Input sequence to start with (start from 0): "))
            en = int(input("Input sequence to end with (end with 15): "))
            if st >= 0 and en <= 15:
                break
        for seq in range(st, en + 1):
            print("---------------------------------------------")
            print(f"Result of INPUT_{seq}.txt:")
            problem = readInput(f"testcases\\INPUT_{seq}.txt")
            print(f"There are {len(problem.items)} items")
            # print(problem)
            if algo == 1:
                elapsedTime, value, solution = BruteForce(problem)
            elif algo == 2:
                elapsedTime, value, solution = BranchAndBound(problem)
            elif algo == 3:
                elapsedTime, value, solution = LocalBeamSearch(problem)
            else:
                elapsedTime, value, solution = GeneticAlgorithm(problem)
                
            print("Executed time (s):", elapsedTime)
            if value != -1:
                print("Best value:", value)
            else:
                solution = [0] * len(problem.items)
                print("No solution found by this algorithm")
            writeOutput(f"OUTPUT_{seq}.txt", value, solution)
        print("\n---------------------------------------------")
        os.system("pause")