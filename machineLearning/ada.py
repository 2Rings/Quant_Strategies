'''
Description: DT_adaboost
@author: huilin
@version: 3
@date: 09/29/2017

'''

import numpy as np
import re
from collections import defaultdict,namedtuple
import uuid
from graphviz import Digraph
import math
import random

#Construct 3 nodes tree
class Node():
    id=0
    def __init__(self):
        self.edges = {}
        self.value=None
        self.node= None

def get_Nodes_Edges(tree=None,root_node=None):
    Node=namedtuple('Node',['id','label'])
    Edge = namedtuple('Edge',['start','end','label'])

    if tree is None:
        tree=tree

    if type(tree) is not dict:
        return [],[]

    nodes,edges=[],[]

    if root_node is None:
        label=list(tree.keys())[0]
        root_node=Node._make([uuid.uuid4(),label])
        nodes.append(root_node)

    for edge_label,sub_tree in tree[root_node.label].items():
        node_label=list(sub_tree.keys())[0] if type(sub_tree) is dict else sub_tree
        sub_node=Node._make([uuid.uuid4(),node_label])
        nodes.append(sub_node)

        edge=Edge._make([root_node,sub_node,edge_label])
        edges.append(edge)

        sub_nodes,sub_edges=get_Nodes_Edges(sub_tree,root_node=sub_node)
            #append more than one values at a time
        nodes.extend(sub_nodes)
        edges.extend(sub_edges)

    return nodes,edges

def dotify(tree=None):
        #Graphviz
    if tree is None:
        tree = tree

    content = 'digraph decision_tree {\n'
    Nodes, Edges = get_Nodes_Edges(tree)

    for node in Nodes:
        content += '    "{}" [label="{}"];\n'.format(node.id, node.label)

    for edge in Edges:
        start, label, end = edge.start, edge.label, edge.end
        content += '    "{}" -> "{}" [label="{}"];\n'.format(start.id, end.id, label)
        content += '}'

    return content

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


def adaboost(x,y, x_test, y_test, attrs, m):
    n = len(y)
    w = [1.0/n for i in range(n)]
    classifier = []
    alpha = []
    Tree_space=buildTree(attrs)
    train_accuracy = []
    test_accuracy = []
    accuracy = {}
    for k in range(m):
        print "m:", k+1
        best_attr, best_error, hm=find_Tree(x,y,w,Tree_space)
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
        plot_model=(classifier,alpha)
        train_accuracy = predict_Adaboost(x,y,plot_model)
        test_accuracy = predict_Adaboost(x_test,y_test,plot_model)
        accuracy[k]=[train_accuracy,test_accuracy]
    return (classifier,alpha),accuracy

def find_Tree(x,y,w,all_Tree):
    best_error = 0.5
    best_attr = []
    n=len(y)
    hm=None
    for tree in all_Tree:
        error = sum(w[i] for i in range(n) if predictDataPoint(x[i],tree)!=y[i])
        if(best_error>error):
            best_error=error
            hm=tree
    print "epsilon:",best_error
    return best_attr, best_error, hm

def buildTree(attrs):
    print "Building Tree..."
    all_Tree=[]
    for node0 in attrs:
        for node11 in attrs:
            for node12 in attrs:
                if(node0 == node11):
                    continue
                if(node0 == node12):
                    continue
                for d0 in [-1,1]:
                    for d1 in [-1,1]:
                        for d2 in [-1,1]:
                            for d3 in [-1,1]:



                                #right,right
                                root_1 = Node()
                                root_1.node=node0
                                leaf0_1=Node()
                                leaf0_1.value=d0
                                right0_1=Node()
                                right0_1.node=node11
                                root_1.edges[0]=leaf0_1
                                root_1.edges[1]=right0_1

                                leaf0_2 = Node()
                                leaf0_2.value = d1
                                right0_2 = Node()
                                right0_2.node = node12
                                right0_1.edges[0]=leaf0_2
                                right0_1.edges[1]=right0_2

                                leaf0_3 = Node()
                                leaf0_3.value = d2
                                leaf0_4 = Node()
                                leaf0_4.value = d3
                                right0_2.edges[0]=leaf0_3
                                right0_2.edges[1]=leaf0_4
                                all_Tree.append(root_1)


                                #left,left
                                root_3 = Node()
                                root_3.node=node0
                                leaf2_1=Node()
                                leaf2_1.value=d0
                                left2_1=Node()
                                left2_1.node=node11
                                root_3.edges[0]=left2_1
                                root_3.edges[1]=leaf2_1

                                leaf2_2 = Node()
                                leaf2_2.value = d1
                                left2_2 = Node()
                                left2_2.node = node12
                                left2_1.edges[0]=left2_2
                                left2_1.edges[1]=leaf2_2

                                leaf2_3 = Node()
                                leaf2_3.value = d2
                                leaf2_4 = Node()
                                leaf2_4.value = d3
                                left2_2.edges[0]=leaf2_3
                                left2_2.edges[1]=leaf2_4

                                all_Tree.append(root_3)

                                #balance
                                root = Node()
                                root.node=node0
                                left=Node()
                                left.node=node11
                                right=Node()
                                right.node=node12
                                root.edges[0]=left
                                root.edges[1]=right

                                leaf0 = Node()
                                leaf0.value = d0
                                leaf1 = Node()
                                leaf1.value = d1
                                left.edges[0]=leaf0
                                left.edges[1]=leaf1

                                leaf2 = Node()
                                leaf2.value = d2
                                leaf3 = Node()
                                leaf3.value = d3
                                right.edges[0]=leaf2
                                right.edges[1]=leaf3

                                all_Tree.append(root)

                                #right,left
                                root_2 = Node()
                                root_2.node=node0
                                leaf1_1=Node()
                                leaf1_1.value=d0
                                right1_1=Node()
                                right1_1.node=node11
                                root_2.edges[0]=leaf1_1
                                root_2.edges[1]=right1_1

                                leaf1_2 = Node()
                                leaf1_2.value = d1
                                left1_2 = Node()
                                left1_2.node = node12
                                right1_1.edges[0]=left1_2
                                right1_1.edges[1]=leaf1_2

                                leaf1_3 = Node()
                                leaf1_3.value = d2
                                leaf1_4 = Node()
                                leaf1_4.value = d3
                                left1_2.edges[0]=leaf1_3
                                left1_2.edges[1]=leaf1_4

                                all_Tree.append(root_2)

                                #left,right
                                root_4 = Node()
                                root_4.node=node0
                                leaf3_1=Node()
                                leaf3_1.value=d0
                                left3_1=Node()
                                left3_1.node=node11
                                root_4.edges[0]=left3_1
                                root_4.edges[1]=leaf3_1

                                leaf3_2 = Node()
                                leaf3_2.value = d1
                                right3_2 = Node()
                                right3_2.node = node12
                                left3_1.edges[0]=leaf3_2
                                left3_1.edges[1]=right3_2

                                leaf3_3 = Node()
                                leaf3_3.value = d2
                                leaf3_4 = Node()
                                leaf3_4.value = d3
                                right3_2.edges[0]=leaf3_3
                                right3_2.edges[1]=leaf3_4

                                all_Tree.append(root_4)
    return all_Tree

def findBest(x,y,w,attrs):
    n=len(y)
    hm=None
    best_error=0.5
    best_attr =[]
    for node0 in attrs:
        for node11 in attrs:
            for node12 in attrs:
                if(node0 == node11):
                    continue
                if(node0 == node12):
                    continue
                for d0 in [-1,1]:
                    for d1 in [-1,1]:
                        for d2 in [-1,1]:
                            for d3 in [-1,1]:



                                #right,right
                                root_1 = Node()
                                root_1.node=node0
                                leaf0_1=Node()
                                leaf0_1.value=d0
                                right0_1=Node()
                                right0_1.node=node11
                                root_1.edges[0]=leaf0_1
                                root_1.edges[1]=right0_1

                                leaf0_2 = Node()
                                leaf0_2.value = d1
                                right0_2 = Node()
                                right0_2.node = node12
                                right0_1.edges[0]=leaf0_2
                                right0_1.edges[1]=right0_2

                                leaf0_3 = Node()
                                leaf0_3.value = d2
                                leaf0_4 = Node()
                                leaf0_4.value = d3
                                right0_2.edges[0]=leaf0_3
                                right0_2.edges[1]=leaf0_4

                                error_2 = sum(w[i] for i in range(n) if predictDataPoint(x[i],root_1)!=y[i])
                                if(best_error>error_2):
                                    best_error=error_2
                                    hm=root_1
                                    best_attr = [node0,node11,node12,d0,d1,d2,d3]


                                #left,left
                                root_3 = Node()
                                root_3.node=node0
                                leaf2_1=Node()
                                leaf2_1.value=d0
                                left2_1=Node()
                                left2_1.node=node11
                                root_3.edges[0]=left2_1
                                root_3.edges[1]=leaf2_1

                                leaf2_2 = Node()
                                leaf2_2.value = d1
                                left2_2 = Node()
                                left2_2.node = node12
                                left2_1.edges[0]=left2_2
                                left2_1.edges[1]=leaf2_2

                                leaf2_3 = Node()
                                leaf2_3.value = d2
                                leaf2_4 = Node()
                                leaf2_4.value = d3
                                left2_2.edges[0]=leaf2_3
                                left2_2.edges[1]=leaf2_4

                                error_4 = sum(w[i] for i in range(n) if predictDataPoint(x[i],root_3)!=y[i])
                                if(best_error>error_4):
                                    best_error=error_4
                                    hm=root_3
                                    best_attr = [node0,node11,node12,d0,d1,d2,d3]

                                #balance
                                root = Node()
                                root.node=node0
                                left=Node()
                                left.node=node11
                                right=Node()
                                right.node=node12
                                root.edges[0]=left
                                root.edges[1]=right

                                leaf0 = Node()
                                leaf0.value = d0
                                leaf1 = Node()
                                leaf1.value = d1
                                left.edges[0]=leaf0
                                left.edges[1]=leaf1

                                leaf2 = Node()
                                leaf2.value = d2
                                leaf3 = Node()
                                leaf3.value = d3
                                right.edges[0]=leaf2
                                right.edges[1]=leaf3

                                error_1 = sum(w[i] for i in range(n) if predictDataPoint(x[i],root)!=y[i])
                                if(best_error>error_1):
                                    best_error=error_1
                                    hm=root
                                    best_attr = [node0,node11,node12,d0,d1,d2,d3]

                                #right,left
                                root_2 = Node()
                                root_2.node=node0
                                leaf1_1=Node()
                                leaf1_1.value=d0
                                right1_1=Node()
                                right1_1.node=node11
                                root_2.edges[0]=leaf1_1
                                root_2.edges[1]=right1_1

                                leaf1_2 = Node()
                                leaf1_2.value = d1
                                left1_2 = Node()
                                left1_2.node = node12
                                right1_1.edges[0]=left1_2
                                right1_1.edges[1]=leaf1_2

                                leaf1_3 = Node()
                                leaf1_3.value = d2
                                leaf1_4 = Node()
                                leaf1_4.value = d3
                                left1_2.edges[0]=leaf1_3
                                left1_2.edges[1]=leaf1_4

                                error_3 = sum(w[i] for i in range(n) if predictDataPoint(x[i],root_2)!=y[i])
                                if(best_error>error_3):
                                    best_error=error_3
                                    hm=root_2
                                    best_attr = [node0,node11,node12,d0,d1,d2,d3]

                                #left,right
                                root_4 = Node()
                                root_4.node=node0
                                leaf3_1=Node()
                                leaf3_1.value=d0
                                left3_1=Node()
                                left3_1.node=node11
                                root_4.edges[0]=left3_1
                                root_4.edges[1]=leaf3_1

                                leaf3_2 = Node()
                                leaf3_2.value = d1
                                right3_2 = Node()
                                right3_2.node = node12
                                left3_1.edges[0]=leaf3_2
                                left3_1.edges[1]=right3_2

                                leaf3_3 = Node()
                                leaf3_3.value = d2
                                leaf3_4 = Node()
                                leaf3_4.value = d3
                                right3_2.edges[0]=leaf3_3
                                right3_2.edges[1]=leaf3_4

                                error_5 = sum(w[i] for i in range(n) if predictDataPoint(x[i],root_4)!=y[i])
                                if(best_error>error_5):
                                    best_error=error_5
                                    hm=root_4
                                    best_attr = [node0,node11,node12,d0,d1,d2,d3]
    print "best_error:", best_error
    return best_attr,best_error,hm

def predictDataPoint(x, N):
    if(N.value is not None):
        return N.value
    next_node=x[N.node]
    return predictDataPoint(x,N.edges[next_node])

def nodes_edges(root):
    tree = {}
    tree[root.node]={}
    if root.value is None:
        tree[root.node][0] = nodes_edges(root.edges[0])
        tree[root.node][1] = nodes_edges(root.edges[1])
    else:
        return root.value
    return tree



def predictDataPoint_1(x, N):
    if(N.value is not None):
        return N.value
    next_node=x[N.node]
    return predictDataPoint_1(x,N.edges[next_node])

def predict_Adaboost(x,y,DT_model):
    y_label=[]
    hm=DT_model[0]
    alpha=DT_model[1]
    m=len(hm)
    for xi in x:
        p = sum([alpha[i]*predictDataPoint_1(xi,hm[i]) for i in range(m)])
        yi = np.sign(p)
        y_label.append(yi)
    error=0.0
    for i in range(len(y_label)):
        if y_label[i] != y[i]:
            error+=1
    return 1-error/len(y_label)

#warn: attr_L is a list, and has attr_idx and attr, they are different, and we want to use idx.
if __name__ == '__main__':

    x_train,y_train=parseFile('heart_train.data')
    x_test,y_test = parseFile('heart_test.data')
    attrs = [i for i in range(22)]
    M=10
    #M=10
    DT_model, accuracy = adaboost(x_train,y_train, x_test, y_test, attrs,M)
    hm = DT_model[0]
    #print "Drawing..."
    #tree = nodes_edges(hm[0])
    #with open('Adaboost_DT[1].dot','w') as f:
    #    dot_0 = dotify(tree)
    #    f.write(dot_0)
    #tree = nodes_edges(hm[1])
    #with open('Adaboost_DT[2].dot','w') as f:
    #    dot_1 = dotify(tree)
    #    f.write(dot_1)
    #tree = nodes_edges(hm[2])
    #with open('Adaboost_DT[3].dot','w') as f:
    #    dot_2 = dotify(tree)
    #    f.write(dot_2)

    print "Training Completed..."
    print "Testing..."
    train_accuracy = predict_Adaboost(x_train,y_train,DT_model)
    test_accuracy = predict_Adaboost(x_test,y_test,DT_model)
    print accuracy
    print "train_accuracy: ", train_accuracy
    print "test_accuracy: ", test_accuracy
