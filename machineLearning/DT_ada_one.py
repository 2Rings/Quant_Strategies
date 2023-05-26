'''
Description: Decision_Tree_Adaboost_OneNode
@author: huilin
@version: 1
@date: 18/10/2017

'''
import numpy as np
import math
import random

class Node():
    id=0
    def __init__(self):
        self.edges = {}
        self.value=None
        self.node= None

def parseFile(fileName):
    file = open(fileName,'rU')
    dataSet = np.loadtxt(file,dtype=int,delimiter=",",ndmin=2)
    y=dataSet[:,0]
    x=dataSet[:,1::]
    num=y.shape[0]
    for i in range(num):
        if y[i]==0:
            y[i]=-1
    return x,y

def adaboost_OneNode(x,y, attrs, m):
    n = len(y)
    w = [1.0/n for i in range(n)]
    classifier= []
    alpha = []
    for i in range(m):
        print "m:", i+1
        best_attr, best_error, hm=findBest(x,y,w,attrs)
        print best_attr
        print best_error
        #if best_error==0:
        #    a=np.inf
        a=0.5*math.log((1-best_error)/best_error)
        for i in range(n):
            #renew weight
            w[i]=(w[i]*math.exp(-y[i]*predictDataPoint(x[i],hm)*a))/(2*math.sqrt(best_error*(1-best_error)))
            print "w_m+1[",i,"]",w[i]
        classifier.append(hm)
        alpha.append(a)
    return (classifier,alpha)

def findBest(x,y,w,attrs):
    n=len(y)
    hm=None
    best_error=0.5
    best_attr =[]
    for node0 in attrs:
        for d0 in [-1,1]:
            for d1 in [-1,1]:
                root = Node()
                root.node=node0
                left = Node()
                left.value = d0
                right=Node()
                right.value = d1
                root.edges[0]=left
                root.edges[1]=right
                error = sum(w[i] for i in range(n) if predictDataPoint(x[i],root)!=y[i])

                if(best_error>error):
                    best_error=error
                    hm=root
                    best_attr = [node0,d0,d1]
    return (best_attr,best_error,hm)

def predictDataPoint(x, N):
    if(N.value is not None):
        return N.value
    next_node=x[N.node]
    return predictDataPoint(x,N.edges[next_node])

def predict_Adaboost(x,y,DT_model):
    y_label=[]
    hm=DT_model[0]
    print "hm:", hm
    alpha=DT_model[1]
    m=len(hm)
    for xi in x:
        p = sum([alpha[i]*predictDataPoint(xi,hm[i]) for i in range(m)])
        yi = np.sign(p)
        y_label.append(yi)

    error=0.0
    for i in range(len(y_label)):
        if y_label[i] != y[i]:
            error+=1
    return 1-error/len(y_label)

if __name__ == '__main__':

    x_train,y_train=parseFile('heart_train.data')
    x_test,y_test = parseFile('heart_test.data')
    attrs=[i for i in range(22)]
    M=20
    DT_Ada_One_model = adaboost_OneNode(x_train,y_train,attrs,M)
    alpha = DT_Ada_One_model[1]
    for i in range(20):
        print "alpha[",i,"]: ", alpha[i]
    print "Training Completed..."
    print "Testing..."
    train_accuracy = predict_Adaboost(x_train,y_train,DT_Ada_One_model)
    test_accuracy = predict_Adaboost(x_test,y_test,DT_Ada_One_model)
    #print DT_Ada_One_model
    print "train_accuracy: ", train_accuracy
    print "test_accuracy: ", test_accuracy
