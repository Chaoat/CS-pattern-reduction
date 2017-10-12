def extract(file_num):
    """
    Reads data from a test file
    :param file_num: The number of the file
    :return: An array containing the data of the test file
    """
    file_num = str(file_num)
    if len(file_num)<5:
        file_num = "0"*(5-len(file_num))+file_num
    file = open("Test Cases/PR_"+file_num+".PRX")
    arr = []
    for item in file:
        arr.append(item.replace("\n", ""))

    PRX0 = [] #0 is num not letter
    index0 = arr.index(" PRX1")
    for i in range(index0):
        PRX0.append(int(arr[i][5:arr[i].find(":")].replace(" ", "")))


    index1 = arr.index(" PRX2")
    temp = "".join(arr[index0+1:index1]).split(" ")
    PRX1 = []
    dictionary = {}
    for item in temp:
        if item != "":
            if item in PRX1:
                dictionary[item] += 1
            else:
                dictionary[item] = 1
            PRX1.append(int(item))
            


    index2 = arr.index(" PRX3")
    index3 = arr.index(" PRX4")
    temp = "".join(arr[index2+1:index3]).split(" ")
    PRX3 = []
    for item in temp:
        if item != "":
            PRX3.append(int(item))

    temp = "".join(arr[index3+1:]).split(" ")
    PRX4 = []
    for item in temp:
        if item != "":
            PRX4.append(int(item))

    return [PRX0,PRX1,dictionary,PRX3,PRX4] #PRX2 is just an array of ones

def ProcessExtraction(file_num):
    """
    Reads a test file and converts it into a dictionary of strips.
    :param file_num: The test file to read
    :return: The strips, size multiplier, and max strip length
    """
    Extraction = extract(file_num)
    StripLength = Extraction[0][1]
    NPAT = Extraction[0][6]
    NPAR = Extraction[0][7]
    SizeMult = NarrowSizes(StripLength, Extraction[1], 100)

    Strips = {}
    for i in range(0, NPAT):
        LocalStrip = []
        for j in range(0, NPAR):
            size = Extraction[1][j]
            amount = Extraction[4][i*NPAR + j]
            for _ in range(0, amount):
                LocalStrip.append(size)
        try:
            Strips[str(LocalStrip)]['amount'] += 1
        except KeyError:
            Strips[str(LocalStrip)] = {'amount':1, 'strip':LocalStrip}
    return [StripLength//SizeMult, SizeMult, Strips]

def NarrowSizes(StripLength, Sizes, maxmult):
    """
    Attempts to find a common factor of all the sizes in the strips
    :param StripLength: The max strip length
    :param Sizes: The strips
    :param maxmult: The largets allowed multiplier
    :return: The highest common factor.
    """
    bestMult = 1
    currentMult = 2
    while currentMult <= maxmult:
        if StripLength%currentMult == 0:
            success = True
            for i in Sizes:
                if i%currentMult != 0:
                    success = False
                    break
            if success:
                bestMult = currentMult
        currentMult += 1

    if bestMult > 0:
        StripLength = StripLength//bestMult
        for i in range(0, len(Sizes)):
            Sizes[i] = Sizes[i]//bestMult

    return bestMult

if __name__ == '__main__':
    print(ProcessExtraction('00001'))
