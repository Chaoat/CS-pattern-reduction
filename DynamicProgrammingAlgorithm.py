import random

def DynamicCuttingStock(sizes, stripSize):
    """
    Dynamicly programmed solver for overall cutting stop problem.
    :param sizes: Sizes, either as a dictionary or a list.
    :param stripSize: The maximum strip length
    :return: A dictionary of the strips.
    """
    sizes = FindSizesFromStrips(sizes)
    Strips = []

    while SizeLeft(sizes) == True:
        NewStrip = FillStrip(sizes, stripSize)
        spaceAvailable = True
        while spaceAvailable == True:
            Strips.append(NewStrip)
            for i in NewStrip:
                sizes[i] += -2
                if sizes[i] < 0:
                    spaceAvailable = False

            for i in NewStrip:
                sizes[i] += 1

    return ProcessStripsIntoDictionary(Strips)

def FindSizesFromStrips(strips):
    """
    Returns a list of sizes that are contained within a number of strips.
    :param strips: The strips to check the sizes for
    :return: The sizes in the strip as a dictionary
    """
    returnSizes = {}
    for strip in strips:
         for i in strips[strip]['strip']:
            try:
                returnSizes[i] += strips[strip]['amount']
            except KeyError:
                returnSizes[i] = strips[strip]['amount']

    return returnSizes

def SizeLeft(sizes):
    """
    Checks whether there are any sizes left.
    :param sizes: The dictionary to check
    :return: True if there is at least one size left, false otherwise.
    """
    for length in sizes:
        if sizes[length] > 0:
            return True
    return False

def FillStrip(sizes, stripSize):
    SizeList = [[]]*(stripSize + 1) #Innitiate a strip of length the strip size, including 0.
    #We want to iterate through every possible size, and find the best way to fill each size up to stripSize.
    #The reason we do this is that it is very easy to find a way to fill a strip if we have access to all the solutions
    #for all the previous strips. For instance, if we want to find strip size 10, and we have size 5, all we need is
    #a solution to a strip of size 5, and then add the 5 size to it to get size 10. This will guarantee us to find
    #a solution that perfectly fits the size, if possible. There are other things that we also take into account, which
    #I will discuss later.
    for i in range(0, stripSize):
        if i > 0 and len(SizeList[i]) == 0:
            SizeList[i] = SizeList[i - 1]
            #If we get to a list size(excluding the first iteration) that means that we have not found a way to fill strip
            #size i. Therefore, we want to fill this solution with the solution before it, and just give away the left over
            #space. I put this in for a very good reason which would be hard to explain, but believe me it would break without this.

        for length in sizes:
            StripPosition = length + i
            if StripPosition <= stripSize:
                NewStrip = QuickSort(SizeList[i] + [length])
                NumberOfCurrentSize = 0
                NewStripDiversity = 0
                NewStripLength = 0
                #There are three things we are considering here.
                #NumberOfCurrentSize: We want to find this, so we know how many pieces of the length we are considering
                #are in the size, as if there are more pieces than we have, this size is impossible and should be
                #discarded.
                #NewStripDiversity: This is a measure of how many different lengths of different sizes are in the size.
                #If we have two solutions that both achieve the required size, we want to choose the more diverse one.
                #This increases the probability of being able to create multiple copies of the same strip.
                #NewStripLength: The length of the new strip. Naturally, if this is longer than the solution there before it,
                #we want to pick the strip of greater length.

                lastj = 0
                for j in NewStrip:
                    if j == length:
                        NumberOfCurrentSize += 1

                    if j != lastj:
                        lastj = j
                        NewStripDiversity += 1
                        #If this size is not the same as the size before it, increase diversity by one. Since the list is
                        #sorted, this will work.

                    NewStripLength += j

                if NumberOfCurrentSize <= sizes[length]:
                    OldStrip = SizeList[StripPosition]
                    OldStripDiversity = 0
                    OldStripLength = 0
                    lastj = 0
                    for j in OldStrip:
                        if j != lastj:
                            lastj = j
                            OldStripDiversity += 1
                        OldStripLength += j

                    #Calculate all the stuff that we did for the new strip, but for the old strip.

                    if OldStripLength == NewStripLength:
                        if NewStripDiversity > OldStripDiversity:
                            SizeList[StripPosition] = NewStrip
                    else:
                        if NewStripLength > OldStripLength:
                            SizeList[StripPosition] = NewStrip

    for i in range(0, stripSize):
        position = stripSize - i
        if len(SizeList[position]) > 0:
            return SizeList[position]
        #This should really just be return the last element.

def QuickSort(sizes):
    """
    Sorts a list of sizes
    :param sizes: The sizes to sort
    :return: The sorted list of sizes
    """
    if len(sizes) > 1:
        pivot = random.randint(0, len(sizes) - 1)
        LowList = []
        HighList = []

        for i in range(0, len(sizes)):
            if i != pivot:
                if sizes[i] < sizes[pivot]:
                    LowList.append(sizes[i])
                else:
                    HighList.append(sizes[i])

        return QuickSort(HighList) + [sizes[pivot]] + QuickSort(LowList)
    else:
        return sizes

def ProcessSizesIntoDictionary(sizes):
    """
    Takes a list of sizes, and processes it into a dictionary of sizes
    :param sizes: The list of sizes
    :return: A dictionary representing the input list of sizes
    """
    returnDictionary = {}
    for i in sizes:
        try:
            returnDictionary[i] += 1
        except KeyError:
            returnDictionary[i] = 1
    return returnDictionary

def ProcessStripsIntoDictionary(sizes):
    """
    Takes a list of strips and turns them into a dictionary of strips
    :param sizes: The strips to convert
    :return: A dictionary representing the input strips
    """
    returnDictionary = {}
    for i in sizes:
        try:
            returnDictionary[str(i)]['amount'] += 1
        except KeyError:
            returnDictionary[str(i)] = {'amount':1, 'strip':i}
    return returnDictionary

#print(DynamicCuttingStock([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5, 5, 5, 5, 5, 5, 5, 5], 10))
#print(DynamicCuttingStock([3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5], 10))
#print(DynamicCuttingStock({138:22, 152:25, 156:12, 171:14, 182:18, 188:18, 193:20, 200:10, 205:12, 210:14, 214:16, 215:18, 220:20}, 560))