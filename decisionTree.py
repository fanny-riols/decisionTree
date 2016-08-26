from Node import *
from prediction import *
from drawTree import *
from Algo import *
from Eval import *
import sys
    
def decisionTree(parameters, types, counts, labels, X, y, algo):
    tree = Node(0, types, counts, labels, X, y, parameters)
    tree.createNode(algo)

    return tree


def checkCriteria(gain, criteria):

    if (gain != "InfoGain" and gain != "GainRatio") or \
                 (criteria != "Entropy" and criteria != "Gini"):
        return False
    return True


def printHelp():
    print("python decisionTree.py [GAIN] [CRITERIA] [Train file] ([Test file])")
    print("Gain:")
    print("\tInfoGain (Information Gain)")
    print("\tGainRatio (Gain Ratio)")
    print("Impurity criteria:")
    print("\tEntropy")
    print("\tGini")


if __name__ == "__main__":

    if len(sys.argv) < 4:
        printHelp()
        sys.exit()

    gain = sys.argv[1]
    criteria = sys.argv[2]

    isOk = checkCriteria(gain, criteria)
    if not isOk:
        printHelp()
        sys.exit()

    algo = Algo(gain, criteria)

    # Create Train data
    parameters, X, y = createData(sys.argv[3], True)
    labels = createLabels(y)
    types, counts = createTypes(X, y, labels, algo)

    # Train
    print("\n\t\t\t\t>>>>>>>>>> TRAIN <<<<<<<<<<\n")
    tree = decisionTree(parameters, types, counts, labels, X, y, algo)
    print(">>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<")
    drawTree(tree)

    ytest = []
    Xtest = []
    ypredict = []

    # Test data
    if len(sys.argv) == 5:
        print("\n\t\t\t\t>>>>>>>>>> TEST <<<<<<<<<<\n")
        parametersTest, Xtest, ytest = createData(sys.argv[4], True)

        ypredict = predictLabels(Xtest, tree)

        success = 0
        if ytest != []:
            for i in range(len(ytest)):
                if ytest[i] == ypredict[i]:
                    success += 1

            success = float(success * 100) / len(ytest)
            print("\nSuccess: " + "%.2f" % success + " %")

    print(ytest)
    print(ypredict)

    evaluation = Eval(ytest, ypredict, labels)
    evaluation.computeErrors()
    print("TP: " + evaluation.tp)
    print("FP: " + evaluation.fp)
    print("TN: " + evaluation.tn)
    print("FN: " + evaluation.fn)

    evaluation.confusionMatrix()
    evaluation.ROC_curve()
    evaluation.precision_recall_curve()
    evaluation.fmeasure(1)
    evaluation.DET_curve()
