import math
from Algo import *

def Entropy(counts):
    # Pour un type en particulier
    entropy = 0

    for i in range(len(counts)):
        num = 0.0
        for j in range(len(counts[i])):
            num += counts[i][j]
        for j in range(len(counts[i])):
            if num != 0 and counts[i][j] != 0:
                a = counts[i][j] / num
                entropy -= float(a * math.log(a, 2))

    return entropy

def Gini(counts):
    # Pour un type en particulier
    gini = 1

    for i in range(len(counts)):
        num = 0.0
        for j in range(len(counts[i])):
            num += counts[i][j]
        for j in range(len(counts[i])):
            if num != 0 and counts[i][j] != 0:
                a = counts[i][j] / num
                gini -= float(a * a)

    return gini



def Information(counts, algo):
    # Pour un type en particulier
    info = 0

    total = 0
    for i in range(len(counts)):
        for j in range(len(counts[i])):
            total += counts[i][j]


    for i in range(len(counts)):
        num = 0.0
        impurity = []

        for j in range(len(counts[i])):
            num += counts[i][j]
        c = []
        for j in range(len(counts[i])):
            if num != 0:
                c.append(counts[i][j] / num)
            else:
                c.append(0)

        if algo.criteria == Criteria.Type['Entropy']:
            impurity = Entropy([c])
        elif algo.criteria == Criteria.Type['Gini']:
            impurity = Gini([c])

        a = num / total
        info += a * impurity


    return info

def InfoGain(counts, numSamples, algo):
    # Pour un type en particulier

    S = []
    total = 0
    numUnknown = 0
    for i in range(len(counts[0])):
        S.append(0)
    for i in range(len(counts)):
        for j in range(len(counts[i])):
            S[j] += counts[i][j]
            total += counts[i][j]
    for i in range(len(S)):
        S[i] = float(S[i]) / total

    impurity = []

    if algo.criteria == Criteria.Type['Entropy']:
        impurity = Entropy([S])
    elif algo.criteria == Criteria.Type['Gini']:
        impurity = Gini([S])

    print('Impurity: ', impurity)

    info = Information(counts, algo)

    print('Info: ', info)

    gain = (float(total) / numSamples) * (impurity - info)

    return gain


def SplitInformation(counts, algo):
    # Pour un type en particulier

    splitInfo = 0

    num = []
    total = 0
    for i in range(len(counts)):
        num.append(0)
        for j in range(len(counts[i])):
            num[i] += counts[i][j]
            total += counts[i][j]

    for i in range(len(num)):
        num[i] = float(num[i]) / total


    if algo.criteria == Criteria.Type['Entropy']:
        splitInfo = Entropy([num])
    elif algo.criteria == Criteria.Type['Gini']:
        splitInfo = Gini([num])

    return splitInfo



def GainRatio(counts, numSamples, algo):
    # Pour un type en particulier

    gain = InfoGain(counts, numSamples, algo)
    splInfo = SplitInformation(counts, algo)

    print(counts)
    print('gain: ', gain)
    print('splInfo: ', splInfo)

    if splInfo != 0:
        gainRatio = gain / splInfo
    else:
        gainRatio = 0


    return gainRatio
