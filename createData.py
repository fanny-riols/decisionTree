from GainRatio import *
import re

def createData(arg, withLabels):

    dataFile = open(arg)
    parameters = []
    data = []

    l = 0
    for line in dataFile:

        line = re.sub('\t', ' ', line)
        for i in range(100):
            line = re.sub('  ', ' ', line)
            line = re.sub(' ', '', line)
        for i in range(20):
            line = re.sub(',,', ',?,', line)
        line = re.sub(' ', ',', line)
        line = re.sub('\n', '', line)
        line = line.split(',')

        if l == 0:
            parameters = line
#del parameters[0]
            del parameters[-1]
            l = 1
            continue

        data.append(line)

    X = []
    y = []

    for i in range(0, len(data)):
        if withLabels:
            X.append(data[i][1 : len(data[i])])
            y.append(data[i][0])
#            X.append(data[i][0 : len(data[i]) - 1])
#           y.append(data[i][len(data[i]) - 1])
        else:
            X.append(data[i][:])

    return (parameters, X, y)


def createLabels(y):
    
    labels = []
    for i in range(len(y)):
        if y[i] not in labels:
            labels.append(y[i])

    labels.sort()

    return labels

def isFloat(string):
    string2 = string.replace('.', '')
    string2 = string2.replace('-', '')
    if string2.isdigit():
        return True
    else:
        return False

def createCounts(types, i, Xt, y, labels, isContinuous):
    c = []
    m = 0
    if len(types[i]) == 1 and isContinuous:
        m = 2
    else:
        m = len(types[i])
    for j in range(m):
        c.append([])
        for k in range(len(labels)):
            c[j].append(0)

    for j in range(len(Xt[i])):
        idx1 = 0
        if Xt[i][j] != '?':
            if len(types[i]) == 1 and isContinuous:
                if float(Xt[i][j]) <= types[i][0]:
                    idx1 = 0
                else:
                    idx1 = 1
            else:
                idx1 = types[i].index(Xt[i][j])
            idx2 = labels.index(y[j])
            c[idx1][idx2] += 1

    return c


def createTypes(X, y, labels, algo):
    types = []
    counts = []


    if len(y) > 1:
        Xt = zip(*X)
    else:
        Xt = zip(*[X])

    Xt = list(Xt)

    for i in range(len(Xt)):
        # TYPES
        types_i = []
        isContinuous = False
        atLeastOneFloat = False
        isContNum = 0

        for j in range(len(Xt[i])):
            if Xt[i][j] not in types_i and Xt[i][j] != '?':
                types_i.append(Xt[i][j])
            if Xt[i][j] == '?' or isFloat(Xt[i][j]):
                isContNum += 1
                if Xt[i][j] != '?':
                    atLeastOneFloat = True

        if isContNum == len(Xt[i]) and atLeastOneFloat:
            isContinuous = True
            gain = []

            A = list(Xt[i])
            A, y2 = zip(*sorted(zip(A, y)))
            #A = [int(x) for x in A]

            Aset = set(A)
            print(Aset)

            for sep in Aset:
                print("sep: ", sep)
                if sep == '?':
                    continue
                sep = float(sep)
                t = [sep]

                c = []
                for k in range(2):
                    c.append([])
                    for j in range(len(labels)):
                        c[k].append(0)
                for k in range(len(A)):
                    if A[k] != '?':
                        idx1 = 0
                        if float(A[k]) <= sep:
                            idx1 = 0
                        else:
                            idx1 = 1
                        idx2 = labels.index(y2[k])
                        c[idx1][idx2] += 1

                g = 0
                if algo.gain == Gain.Type['GainRatio']:
                    g = GainRatio(c, len(X), algo)
                elif algo.gain == Gain.Type['InfoGain']:
                    g = InfoGain(c, len(X), algo)
                gain.append(g)

            mx = max(gain)
            idx = gain.index(mx)
            print(A)
            print(idx)
            print(gain)
            if len(A) > 1 and idx != len(A) - 1 and A[idx + 1] != '?':
                t = (float(A[idx]) + float(A[idx + 1])) / 2
            else:
                t = float(A[idx])
            types_i = [t]

        types.append(types_i)

        # COUNTS
        c = createCounts(types, i, Xt, y, labels, isContinuous)
        counts.append(c)



    return (types, counts)


