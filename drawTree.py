import copy
import pydot

def recursionTree(parent, stringP, graph, repeat, params):
    for i in range(len(parent.childs)):
        # Parent node
        idx = params.index(parent.param)
        #stringP = parent.param + " " + str(repeat[idx])
        labelP = parent.param
        for j in range(len(parent.numLabels)):
            labelP = labelP + "\n" + parent.labels[j] + ": " \
                     + str(parent.numLabels[j])
        labelP += "\nEntropy: " + str("%.4f" %parent.gain)
		#print("label parent: " + labelP)
		#print("NAME parent: " + stringP)
        nodeP = pydot.Node(stringP, shape="box", label=labelP)
        graph.add_node(nodeP)

        # Child node
        stringL = ''
        labelL = ''
        if parent.childs[i].param != 'LEAF':
            idx = params.index(parent.childs[i].param)
            repeat[idx] += 1
            stringL += parent.childs[i].param + " " + str(repeat[idx])
            labelL = parent.childs[i].param
            nodeL = pydot.Node(stringL, shape="box", label=labelL)
            graph.add_node(nodeL)
            edge = pydot.Edge(nodeP, nodeL)
        else:
            stringL = "LEAF " + str(repeat[-1])
            labelL = "-----"
            for j in range(len(parent.numLabels)):
                labelL = labelL + "\n" + parent.childs[i].labels[j] + ": " \
                         + str(parent.childs[i].numLabels[j])
            labelL += "\nEntropy: " + str("%.2f" %parent.childs[i].gain)
            nodeL = pydot.Node(stringL, style="filled",
                    fillcolor="green", shape="box", label=labelL)
            graph.add_node(nodeL)
            edge = pydot.Edge(nodeP, nodeL)
            repeat[-1] += 1
		#print("label child: " + labelL)
		#print("NAME child: " + stringL)

        # print "EDGE"
        edge.set_label(parent.edge[i])
        graph.add_edge(edge)
		#print '\n'
        if parent.childs[i].param != 'LEAF':
            repeat[idx] += 1
		#print "REPEAT: ", repeat
        graph, repeat = recursionTree(parent.childs[i], stringL, graph, repeat,
                params)

	#print "REPEAT: ", repeat
    return (graph, repeat)


def drawTree(tree):
    graph = pydot.Dot(graph_type='digraph')
    parent = copy.copy(tree)
    repeat = []
    for i in range(len(tree.params) + 1):
        repeat.append(0)
    stringP = parent.param + " 0"
    graph, repeat = recursionTree(parent, stringP, graph, repeat, tree.params)

    name = "tree.png"
    graph.write_png(name)
