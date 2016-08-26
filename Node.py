from createData import *
from GainRatio import *
from operator import itemgetter
from Algo import *

class Node:
    def __init__(self, level, types, counts, labels, X, y, params):
        self.param = ''
        self.numLabels = []
        self.childs = []
        self.level = level
        self.mx = 0
        self.edge = []
        self.gain = 0
        self.isCont = False

        self.types = types
        self.counts = counts
        self.labels = labels
        self.X = X
        self.Xt = list(zip(*self.X))
        self.y = y
        self.params = params

    def createNode(self, algo):

        # Count the number of sample for each label
        for i in range(len(self.labels)):
            self.numLabels.append(self.y.count(self.labels[i]))
        
        # Check if more than one label is present
        a = []
        for i in range(len(self.y)):
            if self.y[i] not in a:
                a.append(self.y[i])
        if len(a) == 1:
            self.param = 'LEAF'
            return

        # Compute gain
        gain = []
        for i in range(len(self.counts)):
            if algo.gain == Gain.Type['GainRatio']:
                gain.append(GainRatio(self.counts[i], len(self.X),
                            algo))
            elif algo.gain == Gain.Type['InfoGain']:
                gain.append(InfoGain(self.counts[i], len(self.X), algo))

        # Get the best gain
        self.mx = gain.index(max(gain))
        self.gain = max(gain)
        self.edge = self.types[self.mx][:]
        self.param = self.params[self.mx]

        countLabels = self.numLabels.count(0)

        if len(gain) > 1 and countLabels < len(self.numLabels) - 1:
            m = len(self.types[self.mx])
            if isFloat(str(self.types[self.mx][0])):
                m = 2
                self.isCont = True
                self.edge = ["<= " + str(self.types[self.mx][0]), "> " \
                            + str(self.types[self.mx][0])]

            for i in range(m):
                if not self.isCont:
                    types, counts, X, y, params = self.newNode(self.types[self.mx][i],
                            False, algo)
                else:
                    inf = True
                    if i == 1:
                        inf = False
                    types, counts, X, y, params = self.newNode(self.types[self.mx][0],
                            inf, algo)

                child = Node(self.level + 1, types, counts, self.labels, X, y,
                        params)
                child.createNode(algo)
                self.childs.append(child)
        else:
            self.param = 'LEAF'


    def newNode(self, param, inf, algo):
        indices = []
        if self.isCont:
            l = list(self.Xt[self.mx])
            for i in range(len(l)):
                if inf and float(l[i]) <= param:
                    indices.append(i)
                elif not inf and float(l[i]) > param:
                    indices.append(i)
        else:
            indices = [i for i, k in enumerate(self.Xt[self.mx]) if k == param]

        X = list(itemgetter(*indices)(self.X[:]))
        if len(indices) == 1:
            y = [self.y[indices[0]]]
        else:
            y = list(itemgetter(*indices)(self.y))
        params = self.params[:]
        types, counts = createTypes(X, y, self.labels, algo)

        return (types, counts, X, y, params)
