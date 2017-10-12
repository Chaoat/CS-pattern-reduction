import math

def BinPacking(sizes, stripSize, isStrips):
    """
    A greedy bin packer. Uses the descending first fit algorithm.
    :param sizes: The sizes to pack.
    :param stripSize: The largest allowed strip size
    :param isStrips: Whether the input is sizes or strips
    :return: A dictionary of strips that is the bin packed input sizes
    """
    Strips = [[]]
    SortedSizes = []
    if isStrips:
        SortedSizes = FindSortedSizesFromStrips(sizes)
    else:
        SortedSizes = FindSortedSizesFromSizes(sizes)

    while len(SortedSizes) > 0:
        size = SortedSizes.pop()
        i = 0
        spotFound = False
        while not spotFound:
            if StripTotalSize(Strips[i]) + size <= stripSize:
                Strips[i].append(size)
                spotFound = True
            i += 1
            if i == len(Strips) and not spotFound:
                Strips.append([])
    return(ProcessStripsIntoDictionary(Strips))

def StripTotalSize(Strip):
    """
    Finds the total size of a strip
    :param Strip: The strip
    :return: The total size of the strip
    """
    Size = 0
    for i in Strip:
        Size += i
    return Size

def FindSortedSizesFromStrips(sizes):
    """
    Returns a list of sorted sizes containing the input strips
    :param sizes: The sizes to return a sorted list from
    :return: A sorted list containing the input sizes
    """
    ReturnSizes = []
    for strip in sizes:
        for size in sizes[strip]['strip']:
            BinaryInsert(ReturnSizes, size, sizes[strip]['amount'])
    return ReturnSizes

def FindSortedSizesFromSizes(sizes):
    """
    Returns a list of sorted sizes containing the sizes in the input strips
    :param sizes: The strips to return a sorted list from
    :return: A sorted list containing the input sizes
    """
    ReturnSizes = []
    for size in sizes:
        BinaryInsert(ReturnSizes, size, sizes[size])
    return ReturnSizes

def BinaryInsert(Sizes, size, amount):
    """
    Inserts an element at a given position in a sorted list
    :param Sizes: The list to insert into
    :param size: The element to insert
    :param amount: Amount of the element
    :return: None
    """
    start = 0
    end = len(Sizes) - 1
    while start <= end:
        center = math.ceil((start+end)/2)
        if Sizes[center] == size:
            for _ in range(0, amount):
                Sizes.insert(center, size)
            print(Sizes)
            return
        elif size < Sizes[center]:
            end = center - 1
        else:
            start = center + 1
    center = math.ceil(start+end/2)
    if center > end:
        for _ in range(0, amount):
            Sizes.append(size)
    else:
        for _ in range(0, amount):
            Sizes.insert(center, size)

def ProcessStripsIntoDictionary(sizes):
    """
    Converts a list of strips into a dictionary of strips
    :param sizes: The strips
    :return: The dictionary of the input strips
    """
    returnDictionary = {}
    for i in sizes:
        try:
            returnDictionary[str(i)]['amount'] += 1
        except KeyError:
            returnDictionary[str(i)] = {'amount':1, 'strip':i}
    return returnDictionary

if __name__ == "__main__":
    Sizes = {2:15, 3:10, 5:8}
    print(BinPacking(Sizes, 10, False))