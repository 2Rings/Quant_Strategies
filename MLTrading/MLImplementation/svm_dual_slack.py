'''
Description: SVM_DUAL_SlACK
@author: huilin
@version: 2
@date: 09/17/2017

'''

from cvxopt import matrix
import numpy as np
from cvxopt.solvers import qp
from numpy.linalg import norm

# we want to solve the dual problem with qp(P,q,G,h,A,b)
# therefore these six parameter we need to provide, and we would get alpha as the output

def SVM_alpha(Train_Data,C,sigma):
    global kernelDot
#at first, we need to know information of training data: num and featrues
    num, features=Train_Data.shape
#extract X,y
    X=Train_Data[:,1:features]
    y=Train_Data[:,0]
# P is a mxm matrix, because dim(alpha) = num
    P=matrix(np.zeros((num,num)))
#firstly, compute all the resulet of
    kernel=guassianKernel(X,sigma)
    for i in range(num):
        for j in range(num):
            P[i,j]=y[i]*y[j]*kernel[i,j]

    q=matrix(-1*np.ones((num,1)))

    G=matrix(np.vstack((np.identity(num),-1*np.identity(num))))

    h = matrix(np.zeros((2*num,1)))
    for i in range(num):
        h[i] = float(C)

    A=matrix(np.zeros((1,num)))
    for i in range(num):
        A[i]=y[i]

    b=matrix(np.zeros((1,1)))

#use qp(P,q,G,h,A,b)

    alpha=qp(P,q,G,h,A,b)['x']

    return alpha

def guassianKernel(X,sigma):
    num,featrues=X.shape
    global kernelDot
    for i in range(num):
        for j in range(num):
            # guassianKernel = exp(-||x_i-x_j||^2/(2sigma^2))
            kernelDot[i,j]=np.exp(-1*norm(X[i]-X[j])**2/(2*sigma**2))
    return kernelDot

def bias(Train_Data,alpha,C):
    global kernelDot
    num,features=Train_Data.shape
    X=Train_Data[:,1:]
    y=Train_Data[:,0]
    #Get support vetctor's alpha, store its idx
    sup_alpha_idx=[i for i in range(num) if (alpha[i] > 0 and alpha[i] < C)]
    b=0.0
    #tmp=0.0
    #for j in range(num):
    #    tmp+=y[j]*alpha[sup_alpha_idx[j]]*kernelDot[j,0]
    #b+=y[0]-tmp

    for k in sup_alpha_idx:
        tmp=0.0
        for j in range(num):
            tmp+=y[j]*alpha[j]*kernelDot[k,j]
        b+=y[k]-tmp
    #average
    b/=len(sup_alpha_idx)
    return b

def train_accuracy(Train_Data,alpha,b):
    num_Tr,features=Train_Data.shape
    miss=0.0
    for i in range(num_Tr):
        xi=Train_Data[i,1:features]
        yi=Train_Data[i,0]
        temp=0
        for j in range(num_Tr):
            temp+=alpha[j]*yi*kernelDot[i,j]
        y=temp+b
        if(np.sign(yi)!=np.sign(y)):
            miss+=1
    return 1.0-miss/num_Tr

def test_accuracy(Train_Data,test_Data,alpha,b):
    num_Tr,features=Train_Data.shape
    miss=0.0
    x_train=Train_Data[:,1:features]
    y_train=Train_Data[:,0]
    for d in test_Data:
        xi=d[1:features]
        yi=d[0]
        temp=0
        for j in range(num_Tr):
            temp+=alpha[j]*y_train[j]*np.exp(-1*norm(xi-x_train[j])**2/(2*sigma**2))
        y=temp+b
        if(np.sign(yi)!=np.sign(y)):
            miss+=1
    return 1.0-miss/num_Tr



kernelDot=np.zeros((336,336))
train_Accuracy={}
v_Accuracy={}
test_Accuracy={}

if __name__ == '__main__':
    global kernelDot
    file_train = open("wdbc_train.data",'rU')
    Train_Data=np.loadtxt(file_train,dtype=float,delimiter=',')
    file_validation = open("wdbc_valid.data",'rU')
    v_Data=np.loadtxt(file_validation,dtype=float,delimiter=',')
    file_Test = open("wdbc_test.data",'rU')
    test_Data=np.loadtxt(file_Test,dtype=float,delimiter=',')
    C=[1.0,10.0,100.0,1000.0,10.0**4,10.0**5,10.0**6,10.0**7,10.0**8]
    SIGMA=[0.1,1.0,10.0,100.0,1000.0]
    #C=[10000.0,100000.0]
    #SIGMA=[0.1,10.0,100.0]

    for sigma in SIGMA:
        for c in C:
            alpha=SVM_alpha(Train_Data,c,sigma)
            b=bias(Train_Data,alpha,c)
            train_Accuracy[(sigma,c)]=train_accuracy(Train_Data,alpha,b)
            v_Accuracy[(sigma,c)]=test_accuracy(Train_Data,v_Data,alpha,b)
            test_Accuracy[(sigma,c)]=test_accuracy(Train_Data,test_Data,alpha,b)
            print "Sigma: ", sigma, " C: ", c,
            print "Train_accuracy: ", train_Accuracy[(sigma,c)]
            print "validation_accuracy: ", v_Accuracy[(sigma,c)]
            print "test_Accuracy:", test_Accuracy[(sigma,c)]
