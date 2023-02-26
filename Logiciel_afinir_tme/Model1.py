#import pydotplus
import numpy as np
from sklearn.tree import DecisionTreeClassifier as DTree
from sklearn import tree
from sklearn.neural_network import MLPClassifier
import sklearn
import warnings
from utils import *

warnings.simplefilter('ignore')

# Arbre de decision
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

# Neural Network
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


def test(print_score = False):
    X, Y = getData("data/train.csv")  
    # Classifier
    cf = MLPtrick()
    cf.fit(X,Y)
    if print_score:
        show_counts(Y)
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

def testRaccourci(ratio = 0.2, print_score = False):
    X, Y = getData("data/train.csv") # Load data
    Y = np.array(["Yes"]*len(Y)) # transform label
    X,Y = getNo(X,Y, 10000) # generate false data
    Xtrain, Ytrain, Xtest, Ytest = split(X, Y)

    # Classifier
    cf = MLPtrick()
    cf.fit(Xtrain,Ytrain)
    if print_score:
        getScore(cf,  Xtrain, Ytrain, Xtest, Ytest)
    return cf


if __name__=="__main__":
    testRaccourci(print_score=False)