'''
Description: SVM_SlACK
@author: huilin
@version: 2
@date: 09/20/2017

'''

from cvxopt import matrix
import numpy as np
from cvxopt.solvers import qp

# solution matrix : (weight, cauchy, bias), which makes it very large matrix
def SVM_Slack(Train_Data,C):
    n,m=Train_Data.shape#m=dimX, n=train_num
    m-=1
    mnb=m+n+1 #matrix scale

    X=Train_Data[:,1:m+1]
    y=Train_Data[:,0]
    P=matrix(np.zeros((mnb,mnb)))
    for i in range(m):
        P[i,i]=1.0 # coef matrix of  weight

    q=matrix(np.zeros((mnb,1)))
    for j in range(m,m+n):
        q[j]=C

    G=matrix(np.zeros((n+n,mnb)))
    for k in range(n):
        G[k,:m]=-y[k]*X[k]
        G[k,m+k]=-1.0
        G[k,-1]=-y[k]

    for i in range(n,n+n):
        G[i,m+i-n]=-1.0

    h=matrix(np.zeros((n+n,1)))
    h[:n]=-1.0

    wsb = qp(P,q,G,h)['x']
    return wsb[0:m],wsb[-1]

def validation(V_Data,w,b):
    num,featrues=V_Data.shape
    miss=0.0
    for data in V_Data:
        Xi=data[1:featrues]
        yi=data[0]
        y=np.dot(w.T,Xi)+b
        if(np.sign(yi)!=np.sign(y)):
            miss+=1
    return 1.0-miss/num

def test(test_Data,w,b):
    test_num,featrues=test_Data.shape
    err_count=0.0
    for data in test_Data:
        Xi=data[1:featrues]
        yi=data[0]
        y=np.dot(w.T,Xi)+b
        if(np.sign(yi)!=np.sign(y)):
            err_count+=1
    return 1.0-err_count/test_num


if __name__ == '__main__':
    print "Loading Train_Data ..."
    file_train = open("wdbc_train.data",'rU')
    Train_Data=np.loadtxt(file_train,dtype=float,delimiter=',')
    print "Loading test_Data ..."
    file_validation = open("wdbc_valid.data",'rU')
    v_Data=np.loadtxt(file_validation,dtype=float,delimiter=',')
    print "Loading test_Data ..."
    file_Test = open("wdbc_test.data",'rU')
    test_Data=np.loadtxt(file_Test,dtype=float,delimiter=',')
    C=[1,10,100,1000,10**4,10**5,10**6,10**7,10**8]

    for c in C:
        w,b=SVM_Slack(Train_Data,c)
        accuracy_train=test(Train_Data,w,b)
        accuracy_val=validation(v_Data,w,b)
        accuracy_test=test(test_Data,w,b)
        print "C: "
        print c
        print "w: "
        print w
        print "b: "
        print b
        print "accuracy in Train_Set: "
        print accuracy_train
        print "accuracy in valid_set: "
        print accuracy_val
        print "test_correct_rate: "
        print accuracy_test
