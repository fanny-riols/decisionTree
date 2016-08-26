import copy
import random as rdn

def decideEdge(xi, node):
    if xi[node.mx] == '?':
        edge = []
        for i in range(len(node.types[node.mx])):
            edge.append(i)
        return edge

    edge = 0
    if node.isCont:
        if float(xi[node.mx]) <= node.types[node.mx][0]:
            edge = 0
        else:
            edge = 1
    else:
        edge = node.types[node.mx].index(xi[node.mx])

    return edge

def predictOneLabel(xi, node):
    if node.param == 'LEAF':
        return node

    edge = decideEdge(xi, node)
    #del xi[node.mx]
    
    if isinstance(edge, int) == 1:
        node = copy.copy(node.childs[edge])
        return predictOneLabel(xi, node)

    else:
        nodes = []
        for i in range(len(edge)):
            xi_i = copy.copy(xi)
            node_i = copy.copy(node.childs[edge[i]])
            nodes.append(predictOneLabel(xi_i, node_i))
        return nodes



def predictLabels(X, tree):
    y = []
    for i in range(len(X)):
        y.append(tree.labels[0])

    for i in range(len(X)):
        xi = X[i]
        node = copy.copy(tree)
        node = predictOneLabel(xi, node)

        mx = 0
        idx = 0
        if type(node) is not list:
            for j in range(len(node.labels)):
                if node.numLabels[j] > mx:
                    mx = node.numLabels[j]
                    idx = j
            y[i] = node.labels[idx]

        else:
            proba = []
            for k in range(len(node[0].labels)):
                proba.append(0)
            for j in range(len(node)):
                for k in range(len(node[j].labels)):
                    if float(node[j].numLabels[k]) / len(node[j].y) > proba[k]:
                        proba[k] = float(node[j].numLabels[k]) / len(node[j].y)
            pmax = max(proba)
            pcount = proba.count(pmax)
            if pcount > 1:
                indices = [k for k, x in enumerate(proba) if x == pmax]
                r = rdn.randint(0, len(indices) - 1)
                idx = indices[r]
                y[i] = node[0].labels[idx]
            else:
                 idx = proba.index(pmax)
                 y[i] = node[0].labels[idx]


    return y
