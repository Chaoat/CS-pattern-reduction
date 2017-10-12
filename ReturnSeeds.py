import random

def GenerateDynamicTable(sizes, stripSize):
    """
    Generates the dynamic table which will be used in the dynamic programming knapsacking
    :param sizes: The sizes
    :param stripSize: The largest strip size
    :return: The dynamic table
    """
    DynamicTable = [0]*(stripSize + 1)
    for i in range(0, stripSize + 1):
        DynamicTable[i] = {'currentSolution':[], 'remainingSizes':[], 'previousSolutions':[], 'returned':False}

    DynamicTable[0]['remainingSizes'] = DetermineAvailableSizes(stripSize, sizes)

    ReturnChild(DynamicTable, 0)
    #for i in range(0, stripSize + 1):
    #    if len(DynamicTable[i]['remainingSizes']) > 0:
    #        size = DynamicTable[i]['remainingSizes'].pop()
    #        DynamicTable[i + size]['previousSolutions'].append(DynamicTable[i]['currentSolution'] + [size])
    #        DynamicTable[i + size]['currentSolution'] = DynamicTable[i]['currentSolution'] + [size]
    #        DynamicTable[i + size]['remainingSizes'] = DetermineAvailableSizes(stripSize - i - size, DynamicTable[i]['remainingSizes'])
    #
    #if DynamicTable[stripSize]['currentSolution'] == []:
    #    DynamicTable[stripSize]['currentSolution'] = None

    return DynamicTable

def DetermineAvailableSizes(spaceLeft, sizes):
    """
    Determines what sizes can fit in a remaining space
    :param spaceLeft: The remaining space
    :param sizes: All the sizes
    :return: The subset of sizes representing the sizes that fit in the remaining space
    """
    AvailableSizes = []
    if isinstance(sizes, list):
        for size in sizes:
            if size <= spaceLeft:
                AvailableSizes.append(size)
    else:
        for size in sizes:
            if size <= spaceLeft:
                for _ in range(0, sizes[size]):
                    AvailableSizes.append(size)
    return AvailableSizes


def ReturnChild(DynamicTable, allowedWaste):
    """
    Returns a solution from a dynamic table
    :param DynamicTable: The dynamic table to find the solution from
    :param allowedWaste: The maximum allowed waste in the solution
    :return: The new solution
    """
    TableLength = len(DynamicTable) - 1
    returnSolution = 0
    SolutionPosition = 1

    while SolutionPosition <= allowedWaste:
        if not DynamicTable[TableLength - SolutionPosition]['returned']:
            returnSolution = DynamicTable[TableLength - SolutionPosition]['currentSolution']
            DynamicTable[TableLength - SolutionPosition]['returned'] = True
            break
        SolutionPosition += 1

    if returnSolution == 0:
        returnSolution = DynamicTable[TableLength]['currentSolution']

        NewSolutionFound = False
        backtracking = True
        CurrentPosition = TableLength - 1
        while NewSolutionFound == False:
            if backtracking:
                if len(DynamicTable[CurrentPosition]['remainingSizes']) > 0:
                    size = DynamicTable[CurrentPosition]['remainingSizes'].pop()
                    newSolution = DynamicTable[CurrentPosition]['currentSolution'] + [size]
                    if CheckRepeatSolution(newSolution, DynamicTable[CurrentPosition + size]['previousSolutions']):
                        DynamicTable[CurrentPosition + size]['previousSolutions'].append(newSolution)
                        DynamicTable[CurrentPosition + size]['currentSolution'] = newSolution
                        DynamicTable[CurrentPosition + size]['remainingSizes'] = DetermineAvailableSizes(TableLength - CurrentPosition - size, DynamicTable[CurrentPosition]['remainingSizes'])
                        DynamicTable[CurrentPosition + size]['returned'] = False
                        backtracking = False
                        CurrentPosition = CurrentPosition + size
                else:
                    CurrentPosition = CurrentPosition - 1
            else:
                if CurrentPosition == TableLength:
                    #print(DynamicTable[TableLength]['previousSolutions'])
                    NewSolutionFound = True
                else:
                    if len(DynamicTable[CurrentPosition]['remainingSizes']) > 0:
                        size = DynamicTable[CurrentPosition]['remainingSizes'].pop()
                        newSolution = DynamicTable[CurrentPosition]['currentSolution'] + [size]
                        if CheckRepeatSolution(newSolution, DynamicTable[CurrentPosition + size]['previousSolutions']):
                            DynamicTable[CurrentPosition + size]['previousSolutions'].append(newSolution)
                            DynamicTable[CurrentPosition + size]['currentSolution'] = DynamicTable[CurrentPosition]['currentSolution'] + [size]
                            DynamicTable[CurrentPosition + size]['remainingSizes'] = DetermineAvailableSizes(TableLength - CurrentPosition - size, DynamicTable[CurrentPosition]['remainingSizes'])
                            DynamicTable[CurrentPosition + size]['returned'] = False
                            CurrentPosition = CurrentPosition + size
                    else:
                        backtracking = True
                        CurrentPosition = CurrentPosition - 1

            if CurrentPosition < 0:
                NewSolutionFound = True
                DynamicTable[TableLength]['currentSolution'] = None

    return returnSolution


def CheckRepeatSolution(newSolution, Solutions):
    """
    Checks whether a given solution has already been found
    :param newSolution: The new solution
    :param Solutions: All the previous solutions
    :return: True if solution is not repeat, False if it does repeat
    """
    for solution in Solutions:
        i = 0
        if len(solution) == len(newSolution):
            while solution[i] == newSolution[i]:
                if i + 2 > len(solution):
                    return False
                else:
                    i = i + 1
    return True

#print(DynamicCuttingStock([3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5], 10))
#print(DynamicCuttingStock({138:22, 152:25, 156:12, 171:14, 182:18, 188:18, 193:20, 200:10, 205:12, 210:14, 214:16, 215:18, 220:20}, 560))