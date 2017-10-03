import random
import math
#from DynamicProgrammingAlgorithm import DynamicCuttingStock as BinPacking
from BinPacking import BinPacking as BinPacking

from ReturnSeeds import GenerateDynamicTable
from ReturnSeeds import ReturnChild

class seed():
    def __init__(self, bulk, structure, parent, amount, stripSize, LargerProblem):
        self.LargerProblem = LargerProblem
        self.bins = bulk
        self.children = []
        self.structure = structure
        self.parent = parent
        self.children = []
        self.amount = amount
        self.stripSize = stripSize
        self.seedAmount = GreatestSize(bulk)
        self.allowedWaste = self.CalculateWaste()

        Subset = FindSubsetFromStrips(bulk, self.seedAmount)
        LargerProblem.TimeSpentOther = LargerProblem.TimeSelf(LargerProblem.TimeSpentOther)
        self.table = GenerateDynamicTable(Subset, stripSize)
        LargerProblem.TimeSpentKnapSack = LargerProblem.TimeSelf(LargerProblem.TimeSpentKnapSack)

    def CalculateWaste(self):
        totalUse = 0
        nStrips = 0
        for strip in self.bins:
            nStrips += self.bins[strip]['amount']
            for size in self.bins[strip]['strip']:
                totalUse += size * self.bins[strip]['amount']
        return 1 - totalUse / (nStrips * self.stripSize)

    def getChild(self):
        while self.seedAmount > 1:
            self.LargerProblem.TimeSpentOther = self.LargerProblem.TimeSelf(self.LargerProblem.TimeSpentOther)
            NewSeed = ReturnChild(self.table, 0)
            self.LargerProblem.TimeSpentKnapSack = self.LargerProblem.TimeSelf(self.LargerProblem.TimeSpentKnapSack)
            if NewSeed is not None:
                newBulk = FindBulk(self.bins, NewSeed, self.seedAmount, self.stripSize)
                self.LargerProblem.TimeSpentBinPacking = self.LargerProblem.TimeSelf(self.LargerProblem.TimeSpentBinPacking)
                newSeed = seed(newBulk, NewSeed, self, self.seedAmount, self.stripSize, self.LargerProblem)
                self.children.append(newSeed)
                return newSeed
            else:
                self.seedAmount -= 1
                Subset = FindSubsetFromStrips(self.bins, self.seedAmount)
                self.LargerProblem.TimeSpentOther = self.LargerProblem.TimeSelf(self.LargerProblem.TimeSpentOther)
                self.table = GenerateDynamicTable(Subset, self.stripSize)
                self.LargerProblem.TimeSpentKnapSack = self.LargerProblem.TimeSelf(self.LargerProblem.TimeSpentKnapSack)
        return None

def GreatestSize(strips):
    sizes = FindSubsetFromStrips(strips, 1)
    LargestSize = 0
    for i in sizes:
        if sizes[i] > LargestSize:
            LargestSize = sizes[i]
    return LargestSize

def FindBulk(bulk, seed, amount, stripSize):
    #print(seed)
    #print(bulk)
    BulkSizes = BulkToSizes(bulk)
    #print(BulkSizes)
    for i in seed:
        BulkSizes[i] -= amount

    BulkSizes = BinPacking(BulkSizes, stripSize, False)
    #print(BulkSizes)
    #print('____')
    return BulkSizes

def FindSubsetFromStrips(strips, subset):
    returnSizes = {}
    for strip in strips:
         for i in strips[strip]['strip']:
            try:
                returnSizes[i] += strips[strip]['amount']
            except KeyError:
                returnSizes[i] = strips[strip]['amount']

    RemoveSizes = []
    for number in returnSizes:
        returnSizes[number] = (returnSizes[number])//subset
        if returnSizes[number] == 0:
            RemoveSizes.append(number)

    for i in RemoveSizes:
        del returnSizes[i]

    return returnSizes

def BulkToSizes(bulk):
    Sizes = {}
    for strip in bulk:
        for size in bulk[strip]['strip']:
            try:
                Sizes[size] += bulk[strip]['amount']
            except KeyError:
                Sizes[size] = bulk[strip]['amount']
    return Sizes

def ProcessSizesIntoDictionary(sizes):
    returnDictionary = {}
    for i in sizes:
        try:
            returnDictionary[i] += 1
        except KeyError:
            returnDictionary[i] = 1
    return returnDictionary

def bulk_to_array(bulk):
    output = []
    for key in bulk:
        output += bulk[key]*key
    return output

if __name__ == "__main__":
    StripSize = 10
    Sizes = DynamicCuttingStock([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5, 5, 5, 5, 5, 5, 5, 5], StripSize)

    BaseNode = seed(Sizes, None, None, 0, StripSize)
    NewNode = BaseNode.getChild()