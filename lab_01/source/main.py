def getTabel(file):
    tempTabel = []
    with open(file) as curFile:
        tempTabel = list(map(
            lambda line: tuple(map(float, str(line).split())), curFile))
    return tempTabel


def printTabel(description, tabel):
    print(description, "\nx", "y\n" + "*" * 20, sep="\t")
    list(map(lambda line: print(*line, sep="\t"), tabel))


def findNeedRange(tabel, x, n):
    minList = list(filter(lambda line: line[0] <= x, tabel))
    maxList = list(filter(lambda line: line[0] > x, tabel))

    checkList = lambda curList, n: len(curList) < (n + 1) // 2

    if len(minList + maxList) < n + 1:
        tabel = minList + maxList
    elif checkList(minList, n):
        tabel = minList + maxList[:n + 1 - len(minList)]
    elif checkList(maxList, n):
        tabel = minList[-(n + 1 - len(maxList)):] + maxList
    else:
        stopPoint = (len(minList) > (n // 2) and (n // 2) + 1) or (n // 2)
        tabel = minList[-stopPoint:] + maxList[:(n + 1) - stopPoint]

    return tabel


def interpolation(tabel, x, n):
    calcDiff = lambda xi, xj, yi, yj: ((yi - yj) / (xi - xj))

    needRange = findNeedRange(tabel, x, n)
    listDiff = list(map(lambda line: line[1], needRange))
    resY, mulX, step = listDiff[0], 1, 1

    if len(needRange) <= n: n = len(needRange) - 1

    while len(listDiff) != 1:
        listDiff = list(map(
            lambda i: calcDiff(
                needRange[i][0], needRange[i + step][0],
                listDiff[i], listDiff[i + 1]),
            range(n)))
        mulX *= (x - needRange[0 + step - 1][0])
        resY += mulX * listDiff[0]
        n -= 1
        step += 1

    return resY


def createRangeForBisection(tabel):
    sign = lambda x: 1 if x > 0 else -1
    listRange = []
    finIndex, startInd = 0, 0
    if len(tabel) == 0:
        return None

    curSign = sign(tabel[0][1])
    for i in range(1, len(tabel)):
        if i == len(tabel) - 1:
            finIndex = i
            listRange.append((startInd, finIndex))
        else:
            if sign(tabel[i][1]) == curSign:
                finIndex = i
            elif sign(tabel[i][1]) != curSign:
                curSign = sign(tabel[i][1])
                listRange.append((startInd, finIndex))
                finIndex = i
                startInd = i
    resTabel = []
    if len(listRange) > 1:
        for i in range(len(listRange) - 1):
            resTabel.append(tabel[listRange[i][0]:listRange[i + 1][1] + 1])
    
    return resTabel


def calcRootBisection(tabel, n, eps):
    leftBorder, rightBorder = tabel[0][0], tabel[-1][0]
    mid = (leftBorder + rightBorder) / 2

    while abs(rightBorder - leftBorder) > eps * mid + eps:
        midY = interpolation(tabel, mid, n)
        rightBorderY = interpolation(tabel, rightBorder, n)
        leftBorderY = interpolation(tabel, leftBorder, n)
        
        if  rightBorderY * midY < 0:
            leftBorder = mid
        elif leftBorderY * midY < 0:
            rightBorder = mid
        else:
            if abs(rightBorderY) < 0.001:
                return rightBorder
            elif abs(leftBorderY) < 0.001:
                return leftBorder
            return (leftBorder + rightBorder) / 2
        
        mid = (leftBorder + rightBorder) / 2
    return mid


def createTabelY(tabel):
    tabel = list(map(lambda line: tuple(reversed(line)), tabel))
    tabel.sort(key=lambda list: list[0])
    lastEl = tabel[-1]
    tabel = [tabel[i] for i in range(len(tabel) - 1) if tabel[i][0] < tabel[i + 1][0]]
    tabel.append(lastEl)

    return tabel


if __name__ == "__main__":
    # get tabel
    tabel = getTabel("test.txt")
    printTabel("Исходная таблица", tabel)

    # input x and n
    lineInput = input("\nВведите х и n(через пробел): ").split()
    x, n = float(lineInput[0]), int(lineInput[1])

    y = interpolation(tabel, x, n)
    print("\ny({}) = {}\n".format(x, y))

    tabelY = createTabelY(tabel)
    x = interpolation(tabelY, 0.0, n)
    print("y = 0.0 при x = {}\n".format(x))

    eps = float(input("\nВведите eps: "))
    ansList = createRangeForBisection(tabel)
    if len(ansList) > 0:
        for line in ansList:
            ans = calcRootBisection(line, n, eps)
            print("\nКорень вычесленный сетодом половинного деления =", ans)
    else:
        print("f(x1) * f(x2) > 0")