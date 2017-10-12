from seed_class import seed
from DynamicProgrammingAlgorithm import DynamicCuttingStock as DynamicBinPack
#from BinPacking import BinPacking as BinPacking
from extract import ProcessExtraction
import time

class CuttingStockProblem():
    def __init__(self, Solution, StripSize, runTime):
        """
        The problem with all the inputs. This needs to be called before anything else can happen, and all solving is done
        as functions within this class.
        :param Solution: The initial solution, from which we will be finding reductions.
        :param StripSize: The maximum strip size allowed in the problem.
        :param runTime: The maximum run time allowed to find reductions.
        """
        self.TimeSpentBinPacking = 0
        self.TimeSpentKnapSack = 0
        self.TimeSpentOther = 0

        self.StartTime = 0
        self.LastCheck = 0
        self.MaxRunTime = runTime

        self.StripSize = StripSize
        self.BaseNode = seed(Solution, None, None, 0, StripSize, self)
        self.Nodes = [self.BaseNode]
        self.NodesToExamineStack = [self.BaseNode]

        self.BestSolution = Solution
        self.BestWaste = self.CalculateWaste(Solution)
        self.BestStrips = self.CalculateStrips(Solution)
        self.PrintCurrentSolution()

    def TimeSelf(self, Timer):
        """
        Timing function.
        :param Timer: The timer to add the time to. This coulg be any of the three timers which are maintained
        during the program.
        :return: The new value of the timer
        """
        Timer += time.clock() - self.LastCheck
        self.LastCheck = time.clock()
        return Timer

    def PrintTimes(self):
        """
        Prints all the times taken by the program. Called at the end usually.
        :return: None
        """
        print('Time spent bin packing: ' + str(self.TimeSpentBinPacking))
        print('Time spent knapsack: ' + str(self.TimeSpentKnapSack))
        print('Time spent other: ' + str(self.TimeSpentOther))
        print('Time spent: ' + str(time.clock() - self.StartTime))

    def SolveCuttingStock(self):
        """
        The overall process by which the cutting stock is solved.
        Each node in the tree is examined in turn, until the max runtime is reached.
        :return: The best solution found, as well as the waste of this solution and the number of master strips used.
        """
        self.StartTime = time.clock()

        Halt = False
        while not Halt:
            while len(self.NodesToExamineStack) > 0:
                # print(NodesToExamineStack[len(NodesToExamineStack) - 1].bins)
                self.ExamineNode(self.NodesToExamineStack.pop(len(self.NodesToExamineStack) - 1))
                if self.MaxRunTime < (time.clock() - self.StartTime):
                    break
            if self.MaxRunTime < (time.clock() - self.StartTime):
                break
            for node in self.Nodes:
                self.ExamineNode(node)

            if len(self.NodesToExamineStack) == 0:
                Halt = True

        return [self.BestSolution, 100 * self.BestWaste, self.BestStrips]

    def ExamineNode(self, Node):
        """
        Examines a node, finding 10 children from that name, and adding them to the stack of nodes to be examined.
        :param Node: The node to examine.
        :return: None
        """
        for i in range(10):
            NewNode = Node.getChild()
            if NewNode is not None:
                if not self.IgnoreNewNode(NewNode):
                    self.Nodes.append(NewNode)
                    self.NodesToExamineStack.append(NewNode)
                else:
                    i -= 1
            else:
                if i == 0:
                    Solution = self.CompileSolution(Node)
                    if self.UpdateSolution(Solution):
                        self.PrintCurrentSolution()
                break

    def IgnoreNewNode(self, NewNode):
        """
        Checks whether a new node should be ignored.
        Currently this only happens if the new node has more strips in its seed pattern than the best found so far +1.
        Given further development, this is one of the aspects that should be looked into in greater detail.
        :param NewNode: The node to check
        :return: True if the node should be ignored, false otherwise.
        """
        NodeSeed = NewNode.structure
        Parent = NewNode.parent

        while Parent is not None: #Checks to see if any of the parents of the node have the same seed pattern as the new node.
            if NodeSeed == Parent.structure:
                return True
            else:
                Parent = Parent.parent

        Solution = self.CompileSolution(NewNode)
        if self.CalculateStrips(Solution) > self.BestStrips + 1:
            return True
        #if self.CalculateWaste(Solution) > self.BestWaste:
            #return True

        return False

    def UpdateSolution(self, Solution):
        """
        Checks whether the solution is the best solution found so far.
        :param Solution: The solution to check.
        :return: True if the new solkution is better, false if not.
        """
        newWaste = self.CalculateWaste(Solution)
        newStrips = self.CalculateStrips(Solution)

        if newStrips < self.BestStrips:
            self.BestSolution = Solution
            self.BestWaste = newWaste
            self.BestStrips = newStrips
            return True
        elif newStrips == self.BestStrips:
            if newWaste < self.BestWaste:
                self.BestSolution = Solution
                self.BestWaste = newWaste
                self.BestStrips = newStrips
                return True
        print('Solution: ' + str(Solution))
        print('Waste: ' + str(100 * newWaste) + '%')
        print('MasterStrips: ' + str(newStrips))
        print('---------- Solution rejected')
        return False

    def PrintCurrentSolution(self):
        """
        Prints the current best solution.
        :return: None
        """
        print('Solution: ' + str(self.BestSolution))
        print('Waste: ' + str(100 * self.BestWaste) + '%')
        print('MasterStrips: ' + str(self.BestStrips))
        print('---------- Best solution')

    def CalculateWaste(self, Solution):
        """
        Calculates the amount of waste in a certain solution.
        :param Solution: The solution to check
        :return: The amount of waste in the solution (returned as a float between 0 and 1.)
        """
        totalUse = 0
        nStrips = 0
        for strip in Solution:
            nStrips += Solution[strip]['amount']
            for size in Solution[strip]['strip']:
                totalUse += size*Solution[strip]['amount']
        return 1 - totalUse/(nStrips*self.StripSize)

    def CalculateStrips(self, Solution):
        """
        Calculates the number of master strips used in a solution.
        :param Solution: The solution to check
        :return: The amount of master strips used.
        """
        nStrips = 0
        for strip in Solution:
            nStrips += 1

        return nStrips

    def CompileSolution(self, Node):
        """
        Finds all the seed patterns of the parents of the node and compiles them into a solution.
        :param Node: The node to compile the solution from.
        :return: The solution
        """
        Solution = {}

        for bin in Node.bins:
            try:
                Solution[str(bin)][Node.bins[bin]['amount']] += Node.bins[bin]['amount']
            except KeyError:
                Solution[str(bin)] = {'amount': Node.bins[bin]['amount'], 'strip': Node.bins[bin]['strip']}

        while Node.parent is not None:
            try:
                Solution[str(Node.structure)]['amount'] += Node.amount
            except KeyError:
                Solution[str(Node.structure)] = {'amount': Node.amount, 'strip': Node.structure}
            Node = Node.parent
        return Solution

def RemultiplySolution(Solution, SizeMultiplier):
    """
    Multiplies all the sizes in the solution by the multiplier originally divided by.
    :param Solution: Solution to multiply
    :param SizeMultiplier: Multiplier
    :return: The multiplied solution
    """
    MultipliedSolution = {}
    for strip in Solution:
        numbers = strip.strip('[')
        numbers = numbers.strip(']')
        numbers = numbers.split(', ')
        for i in range(len(numbers)):
            numbers[i] = int(numbers[i])*SizeMultiplier
        MultipliedSolution[str(numbers)] = {'amount':Solution[strip]['amount'], 'strip':[]}
        for i in Solution[strip]['strip']:
            MultipliedSolution[str(numbers)]['strip'].append(i*SizeMultiplier)
    return MultipliedSolution

def RunTestData(file_num, runTime):
    """
    Runs some test data, prints the results.
    :param file_num: The data to run
    :param runTime: The time to run it for
    :return: None
    """
    TestData = ProcessExtraction(file_num)
    Strips = TestData[2]
    StripSize = TestData[0]
    SizeMult = TestData[1]

    Problem = CuttingStockProblem(Strips, StripSize, runTime)
    Solution = Problem.SolveCuttingStock()
    Solution[0] = RemultiplySolution(Solution[0], SizeMult)
    print('Strips: ' + str(Solution[0]))
    print('Waste: ' + str(Solution[1]) + '%')
    print('NStrips used: ' + str(Solution[2]))

    Problem.PrintTimes()

if __name__ == '__main__':
    #StripSize = 560
    #Sizes = {138:22, 152:25, 156:12, 171:14, 182:18, 188:18, 193:20, 200:10, 205:12, 210:14, 214:16, 215:18, 220:20}
    #StripSize = 10
    #Sizes = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5]
    #StripSize = 10
    #Sizes = {2:15, 3:10, 5:8}

    #Sizes = BinPacking(Sizes, StripSize, False)
    RunTestData('00001', 30)

