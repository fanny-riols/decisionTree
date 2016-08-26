import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from ggplot import *
from sklearn.metrics import *

class Eval():
    def __init__(self, y, pred, labels):
        self.y = y
        self.y01 = []
        self.pred = pred
        self.pred01 = []
        self.labels = labels

        self.fp = 0.
        self.tp = 0.
        self.p = 0.

        self.fn = 0.
        self.tn = 0.
        self.n = 0.

        self.cm = []
        self.auc = []


    def computeErrors(self):
        print("Compute False/True Positive/Negative")
        for i in range(len(self.y)):
            yi = self.y[i]
            yhi = self.pred[i]
            if yi == 'Yes' or yi == 'yes' or yi == 'true' or yi == 'True' \
                    or yi == True or yi == 1:
                self.y01.append(1)
                if yi == yhi:
                    self.tp += 1
                    self.pred01.append(1)
                else:
                    self.fn += 1
                    self.pred01.append(0)
            else:
                self.y01.append(0)
                if yi == yhi:
                    self.tn += 1
                    self.pred01.append(0)
                else:
                    self.fp += 1
                    self.pred01.append(1)


        self.p = self.tp + self.fn
        self.n = self.fp + self.tn

    def plot_confusion_matrix(self):
        plt.imshow(self.cm, interpolation='nearest')
        plt.title('Confusion matrix')
        plt.colorbar()
        tick_marks = np.arange(len(self.labels))
        plt.xticks(tick_marks, self.labels, rotation=45)
        plt.yticks(tick_marks, self.labels)
        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        for x in range(len(self.cm)):
            for y in range(len(self.cm[x])):
                plt.annotate(str(self.cm[x][y]), xy=(y, x))


    def confusionMatrix(self):
        self.cm = confusion_matrix(self.y, self.pred)
        plt.figure()
        self.plot_confusion_matrix()
        plt.savefig('confusion_matrix.png')


    def DET_curve(self):
        fpr, tpr, _ = roc_curve(self.y01, self.pred01)
        fnr = []
        for i in range(len(tpr)):
            fpr[i] *= self.n
            tpr[i] *= self.p
            fnr.append(self.p - tpr[i])
        print(fpr)
        print(fnr)

        df = pd.DataFrame(fpr, fnr)
        det = ggplot(df, aes(x=fpr, y=fnr), log='y') \
                + geom_line() \
                + xlab("False Positive Rate") + ylab("False Negative Rate") \
                + scale_x_log10() + scale_y_log10() \
                + ggtitle("Detection Error Tradeoff (DET) curve")
        ggsave(det, 'DET')


    def ROC_curve(self):
        fpr, tpr, _ = roc_curve(self.y01, self.pred01)
        auc_roc = auc(fpr, tpr)
        df = pd.DataFrame(fpr, tpr)
        pauc = ggplot(df, aes(x='fpr', ymin=0, ymax='tpr')) \
                + geom_area(alpha=0.2) \
                + xlab("True Positive Rate") + ylab("False Positive Rate") \
                + geom_line(aes(y='tpr')) \
                + ggtitle("ROC Curve | AUC = %s" % str(auc_roc))
        ggsave(pauc, 'ROC')
        print("AUC:\t\t\t", auc_roc)
        print("GINI COEFFICIENT:\t", 2 * auc_roc - 1)


    def precision_recall_curve(self):
        precision, recall, _ = precision_recall_curve(self.y01, self.pred01)
        avg = average_precision_score(self.y01, self.pred01)
        df = pd.DataFrame(precision, recall)
        pr = ggplot(df, aes(x=precision, y=recall)) \
                + geom_line() \
                + xlab("Precision") + ylab("Recall") \
                + ggtitle("Precision-Recall curve | AVG = %s" % str(avg))
        ggsave(pr, 'Precision-Recall')


    def fmeasure(self, beta):
        beta = float(beta)
        recall = self.recall()
        precision = self.precision()
        print(recall)
        print(precision)

        fm = ((1 + beta * beta) * recall * precision) \
                / (beta * beta * recall + precision)

        print("F MEASURE:\t\t", fm)


    def accuracy(self):
    # Good classification rate
        return (self.tp + self.tn) / (self.p + self.n)


    def recall(self):
    # Recall, true positive rate, sensitivity
        return self.tp / self.p

    def recallRate(self, tp, p):
    # Recall, true positive rate, sensitivity
        return tp / p


    def falseAlarm(self):
    # False alarm rate, false positive rate
        return self.fp / self.n

    def falseAlarmRate(self, fp, n):
    # False alarm rate, false positive rate
        return fp / n


    def miss(self):
    # Missed detection rate, false negative rate
        return self.fn / self.p


    def specificity(self):
    # Specificity, true negative rate
        return 1 - self.falseAlarm()


    def precision(self):
    # Precision
        return self.tp / (self.tp + self.fp)


    def fscore(self):
    # F-score
        return self.precision() * self.recall()
