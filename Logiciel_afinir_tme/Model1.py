#import pydotplus
import numpy as np
import pandas as pd
from sklearn.linear_model import Perceptron
from sklearn.tree import DecisionTreeClassifier as DTree
from sklearn import tree
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize

import matplotlib.pyplot as plt
import time
import sklearn
import warnings


def getData():
    print("GetData")
    df = pd.read_csv("data/train.csv")
    df = df.drop_duplicates()
    X = df.to_numpy()
    X,Y = X[:,:-1], X[:,-1]
    return X,Y

def generateData():
    PlayerBacic.PlayerBasic()

class Tree():
    def __init__(self):
        self.model = DTree()
        self.enc = sklearn.preprocessing.OneHotEncoder()
    def fit(self, X, Y):
        self.enc.fit(X)
        self.model.fit(self.enc.transform(X).toarray(), Y)

    def predict(self, x):
        return self.model.predict(self.enc.transform(x).toarray())
    
    def score(self, X, Y):
        return self.model.score(self.enc.transform(X).toarray(),Y)
    
class MLPtrick():
    def __init__(self):
        self.model=MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5), random_state=1)
    def fit(self,X,Y):
        n, d  = X.shape
        newX = np.zeros((n,3))
        for i in range(3):
            newX[:,i] = X[:,i] - X[:,i+3]
        
        self.model.fit(newX,Y)
    def predict(self,x):
        x = np.asarray(x)
        n, d  = x.shape
        newX = np.zeros((n,3))
        for i in range(3):
            newX[:,i] = x[:,i] - x[:,i+3]
        
        return self.model.predict(newX)
    
    def score(self,x,Y):
        n, d  = x.shape
        newX = np.zeros((n,3))
        for i in range(3):
            newX[:,i] = x[:,i] - x[:,i+3]
        
        return self.model.score(newX,Y)
    
    def predict_proba(self,x):
        x = np.asarray(x)
        n, d  = x.shape
        newX = np.zeros((n,3))
        for i in range(3):
            newX[:,i] = x[:,i] - x[:,i+3]
        
        return self.model.predict_proba(newX)

def getNo(X,Y):
    n,d = X.shape
    c = d//2
    E = np.array(X[:,:c]).astype("<U22")
    print(E.shape)
    etatInital = np.unique(E, axis=0)
    L = []
    i = 0
    for e in etatInital:
        etatFinal = X[np.where(e == X[:,:c], 0, 1)][:,c:]
        print("Before ", etatFinal.shape)
        etatFinal = np.unique(etatFinal.astype("<U22"), axis=0)
        print(etatFinal.shape)
        for e1 in etatFinal:
            L.append(flatten_list([e, e1]))
            i+=1
    L = np.array(L)
    print("L", L.shape)
    print("X; ", X.shape)
    print(L)
    newX = np.concatenate((X, L), axis = 0)
    newY =  np.concatenate((Y, ["No"]*i), axis = 0)
    return newX, newY
    
def flatten_list(_2d_list):
    flat_list = []
    # Iterate through the outer list
    for element in _2d_list:
        if type(element) is list or type(element) is tuple:
            # If the element is of type list, iterate through the sublist
            flat_list.extend(flatten_list(element))
        else:
            flat_list.append(element)
    return flat_list    
        

def test():
    warnings.simplefilter('ignore')
    X, Y = getData()  
    print("Taille X: ", X.shape)
    #X,Y =  getNo(X,Y)
    n, d  = X.shape

    #print(X,Y)
    #X = normalize(X, axis = 0, norm='l1')
    # Classifier
    cf = MLPtrick()#Tree()
    cf.fit(X,Y)
    prediction = cf.predict(X)
    print("\nscore: ", cf.score(X,Y))
    for y in np.unique(Y):
        indices = Y == y
        print("Y: ", y, " - ", cf.score(X[indices],Y[indices]))
        v,c = np.unique(prediction[indices][prediction[indices]!=y], return_counts=True)
        for i in range(len(v)):
            print("\t",v[i], " - ", c[i])
        print()
    return cf




if __name__=="__main__":
    test()

