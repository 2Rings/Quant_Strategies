'''
Description: coordinate_Decent
@author: huilin
@version: 1
@date: 18/10/2017

'''
import numpy as np
import math
import random
from collections import defaultdict,namedtuple
import uuid
from graphviz import Digraph

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

def coordinate_Decent(x,y,attrs):
    n=len(y)
    T=len(attrs)*4
    ht=[]
    alpha=[0 for i in range(T)]
    for node0 in attrs:
        for d0 in [-1,1]:
            for d1 in [-1,1]:
                root = Node()
                root.node = node0
                left = Node()
                left.value = d0
                right = Node()
                right.value = d1
                root.edges[0]=left
                root.edges[1]=right
                ht.append(root)
    for t in range(T):
        nume = 0.0
        deno = 0.0
        for i in range(n):
            if predictDataPoint(x[i],ht[t])==y[i]:
                nume = nume + math.exp(-y[i]*sum([alpha[j]*predictDataPoint(x[i],ht[j]) for j in range(T) if j!= t]))
            else:
                deno = deno + math.exp(-y[i]*sum([alpha[j]*predictDataPoint(x[i],ht[j]) for j in range(T) if j!= t]))
        alpha[t]= 0.5*math.log(nume/deno)
    return (ht,alpha)

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

def exp_Loss(x,y,DT_model):
    Loss=0.0
    n=len(y)
    ht = DT_model[0]
    alpha = DT_model[1]
    T= len(alpha)
    for i in range(n):
        Loss = Loss + math.exp(-y[i]*sum([alpha[j]*predictDataPoint(x[i],ht[j]) for j in range(T)]))
    return Loss

def nodes_edges(root):
    tree = {}
    tree[root.node]={}
    if root.value is None:
        tree[root.node][0] = nodes_edges(root.edges[0])
        tree[root.node][1] = nodes_edges(root.edges[1])
    else:
        return root.value

    return tree

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

if __name__ == '__main__':

    x_train,y_train = parseFile('heart_train.data')
    x_test,y_test = parseFile('heart_test.data')
    attrs = [i for i in range(22)]

    DT_CD_model = coordinate_Decent(x_train,y_train,attrs)
    alpha = DT_CD_model[1]
    ht = DT_CD_model[0]
    #for i in range(len(ht)):
    tree = nodes_edges(ht[0])
    #drawing
    print "Drawing..."
    with open('cd.dot','w') as f:
        dot = dotify(tree)
        f.write(dot)

    print "Training Completed..."
    for i in range(88):
        print "alpha[",i,"]: ", alpha[i]
    print "Testing..."
    train_accuracy = predict_Adaboost(x_train,y_train,DT_CD_model)
    test_accuracy = predict_Adaboost(x_test,y_test,DT_CD_model)
    print "Computing Loss"
    loss= exp_Loss(x_train, y_train, DT_CD_model)
    print "Loss: ", loss

    print "train_accuracy: ", train_accuracy
    print "test_accuracy: ", test_accuracy
    print tree
