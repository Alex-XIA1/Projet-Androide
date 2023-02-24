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
from scipy.stats import itemfreq
import matplotlib.pyplot as plt
import time
import sklearn
import warnings
import PlayerBasic


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

# Add data
# rows, impossible transition with label "No"
def getNo(X,Y, max_n):
    c = X.shape[1]//2
    X = X.astype(int)
    newX = X
    ratio = 0.5
    coupe_n = int(len(newX)*ratio)
    etatInital = np.unique(newX[:,:c], axis=0)[:coupe_n]
    L = [] # list of added rows
    i = 0 # number of added rows
    for e in etatInital: 
        # indices des etats impossibles depuis l'état e
        indices = np.where(e != X[:,:c])[0][:1]
        if len(indices) == 0: continue
        # On supprime les duplicatas
        etatFinal = np.unique(X[:,c:][indices], axis=0)
        # On ajoutes les lignes
        for e1 in etatFinal:
            L.append(flatten_list([e, e1]))
            i+=1
        if i>=max_n:
            break
    L = np.array(L)
    print("Generate %d data" %i)
    return np.concatenate((X, L), axis = 0), np.concatenate((Y, ["No"]*i), axis = 0)
    
def flatten_list(_2d_list):
    flat_list = []
    # Iterate through the outer list
    for element in _2d_list:
        if type(element) is list or type(element) is tuple or type(element) is np.ndarray:
            # If the element is of type list, iterate through the sublist
            flat_list.extend(flatten_list(element))
        else:
            flat_list.append(element)
    return flat_list    
        
def show_stats(data, text = None):
    V,C = np.unique(data, return_counts = True)
    if text == None:
        print("========= Stats ==========")
    print(" Value  |  Counts")
    for i in range(len(C)):
        print(V[i], '  -  ', C[i])
    print("==========================")

warnings.simplefilter('ignore')

def test():
    X, Y = getData()  
    X,Y = getNo(X,Y)
    show_stats(Y)
    n, d  = X.shape

    # Classifier
    cf = MLPtrick()
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

def testData(X,Y):
    avant = len(X)
    assert len(np.unique(X, axis=0)) == avant


def testRaccourci():
    X, Y = getData()
    n,d = X.shape  
    Y = np.array(["Yes"]*n)
    X,Y = getNo(X,Y, 10000)
    testData(X,Y)
    show_stats(Y)
    ratio = 0.2
    n_coupe = int(n*ratio)
    Xtrain, Ytrain = X[:n_coupe], Y[:n_coupe]
    Xtest, Ytest = X[n_coupe:], Y[n_coupe:]

    # Classifier
    cf = MLPtrick()
    cf.fit(Xtrain,Ytrain)
    prediction = cf.predict(Xtest)
    print("\n============== score: ===================")
    print("Paramters: train (%d), test(%d)" % (len(Ytrain), len(Ytest)))
    print("train: ", cf.score(Xtrain,Ytrain))
    print("test: ", cf.score(Xtest,Ytest))
    for y in np.unique(Ytest):
        indices = Ytest == y
        print("Y: ", y, " - ", cf.score(Xtest[indices],Ytest[indices]))
        v,c = np.unique(prediction[indices][prediction[indices]!=y], return_counts=True)
        for i in range(len(v)):
            print("\t",v[i], " - ", c[i])
        print()
    return cf


if __name__=="__main__":
    testRaccourci()