'''
Description: Decision_Tree_ID3
@author: huilin
@version: 2
@date: 09/20/2017

'''
import numpy as np
import math
from numpy.linalg import norm


#normalize
def normalize(X):
    num,featrues=X.shape
    X_min=X.min(axis=0)
    X_range=(X-X_min).max(axis=0)
    X_normalize=(X-X_min)/X_range
    return X_normalize

#find k_nearest
def getNeighbors(X_Train,test_Instance,k):
    k_point=distanceLp(X_Train,test_Instance,k)
    #print dist
    return k_point

#Euclid
def distanceLp(X_Train, test_Instance,k):
    num,featrues=X_Train.shape
    #dist=np.zeros((num,1))
    dist={}
    for i in range(num):
        k_point=[]
        dist[norm(X_Train[i]-test_Instance)]=i
    k_dist=sorted(dist.keys())
    for k_th in range(k):
        k_point.append(dist[k_dist[k_th]])#knearest list
    return k_point

#Assign label for X_test
def getLable(X_Train, y_Train, test_Instance,k):
    knearest=getNeighbors(X_Train, test_Instance,k)
    label=0
    for k_th in range(k):
        if(y_Train[knearest[k_th]]==-1):
            label+=1
    return -1 if label > k-label else 1


def parseFile(Data):
    num,features=Data.shape
    X=Data[:,1:]
    y=Data[:,0]
    X=normalize(X)
    return X,y

if __name__ == '__main__':
    print "Loading Train_Data ..."
    train_file=open("wdbc_train.data",'rU')
    Train_Data=np.loadtxt(train_file,dtype=float,delimiter=',')
    print "Loading test_Data ..."
    test_file=open("wdbc_test.data",'rU')
    test_Data=np.loadtxt(test_file,dtype=float,delimiter=',')
    print "Loading test_Data ..."
    val_file=open("wdbc_valid.data",'rU')
    val_Data=np.loadtxt(val_file,dtype=float,delimiter=',')
    X_train,y_train=parseFile(Train_Data)
    X_test, y_test=parseFile(test_Data)
    X_val, y_val=parseFile(val_Data)
    num_test=test_Data.shape[0]
    num_train=Train_Data.shape[0]
    num_valid=val_Data.shape[0]
    y_pridict=0
    K=[1,5,11,15,21]
    for k in K:
        err_train=0.0
        for i in range(num_train):
            y_predict_train=getLable(X_train,y_train, X_train[i], k)
                    #print np.sign(y_predict),np.sign(y_test[i])
            if(np.sign(y_predict_train)!=np.sign(y_train[i])):
                err_train+=1
        err_test=0.0

        for j in range(num_test):
            y_predict=getLable(X_train,y_train, X_test[j], k)
            #print np.sign(y_predict),np.sign(y_test[i])
            if(np.sign(y_predict)!=np.sign(y_test[j])):
                err_test+=1

        err_val=0.0
        for m in range(num_valid):
            y_predict_valid=getLable(X_train,y_train, X_val[m], k)
            #print np.sign(y_predict),np.sign(y_test[i])
            if(np.sign(y_predict_valid)!=np.sign(y_val[m])):
                err_val+=1
        print "k: ",k
        print "accuracy_train: ", 1.0-float(err_train/num_train)
        print "accuracy_val: ", 1.0-float(err_val/num_valid)
        print "accuracy_test: ",  1.0-float(err_test/num_test)
