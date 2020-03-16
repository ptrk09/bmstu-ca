def getTabel(file):
    tempTabel = []
    with open(file) as curFile:
        tempTabel = list(map(
            lambda line: tuple(map(float, str(line).split())), curFile))
    return tempTabel


def printTabel(description, tabel):
    print(description, "\nx", "y", "z\n" + "*" * 20, sep="\t")
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


def findPointByX(tabel, x, y, ny):
    tempTabel = tabel[:]
    tempTabel = list(filter(lambda line: line[0] == x, tempTabel))
    tempTabel = list(map(lambda line: line[1:], tempTabel))
    return interpolation(tempTabel, y, ny)
    

def createTabel4calcZ(tabel, y, ny):
    listAllX = tuple(sorted(set((map(lambda el: el[0], tabel)))))
    listAllZ = tuple(map(lambda el: findPointByX(tabel, el, y, ny), listAllX))
    return list(map(lambda *args: tuple(args), listAllX, listAllZ))


if __name__ == "__main__":
    # get tabel
    tabel = getTabel("test.txt")
    printTabel("Исходная таблица", tabel)

    # input x, y and nx, ny
    x, y = map(float, input("\nВведите х и y(через пробел): ").split())
    nx, ny = map(int, input("\nВведите nx и ny(через пробел): ").split())

    curTabel = createTabel4calcZ(tabel, y, ny)
    resZ = interpolation(curTabel, x, nx)
    
    print("\nz = {}".format(resZ))