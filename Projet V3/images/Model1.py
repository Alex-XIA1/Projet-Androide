#import pydotplus
import numpy as np
from sklearn.tree import DecisionTreeClassifier as DTree
from sklearn import tree
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
import sklearn
import warnings
from utils import *
from sklearn.neighbors import KNeighborsClassifier as KNN
from time import time

warnings.simplefilter('ignore')

# Arbre de decision
class Tree():
    def __init__(self):
        self.model = DTree()
        #self.enc = sklearn.preprocessing.OneHotEncoder()
    
    def fit(self, X, Y):
        #X = self.enc.fit(X)
        self.model.fit(X.toarray(), Y)

    def predict(self, x):
        #x = self.enc.transform(x)
        return self.model.predict(x.toarray())
    
    def score(self, X, Y):
        #x = self.enc.transform(X)
        return self.model.score(X.toarray(),Y)

# Neural Network
class MLPtrick():
    def __init__(self):
        #self.model=MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5), random_state=1)
        #self.model= KNN(n_neighbors = 700)
        #self.model = SVC(probability=True, kernel='poly')
        self.model = DTree()
    
    def fit(self,x,y):
        x = np.asarray(x)
        n, d  = x.shape
        newX = np.zeros((n,3))
        for i in range(3):
            newX[:,i] = x[:,i] - x[:,i+3]
        newX = newX.astype(int)
        self.model.fit(newX, y)
    
    def predict(self,x):
        return self.model.predict(self.transform(x))
    
    def score(self,x,y):
        return self.model.score(self.transform(x), y)
    
    def predict_proba(self,x):     
        return self.model.predict_proba(self.transform(x))
    
    def transform(self, x):
        x = np.asarray(x)
        n, d  = x.shape
        newX = np.zeros((n,3))
        for i in range(3):
            newX[:,i] = x[:,i] - x[:,i+3]
        return newX
    
    def afficheConfiance(self, x):
        classes= self.model.classes_
        print("=============== Confiance =================")
        Lconfiance = np.around((self.predict_proba(x)[0]), 3)
        confiance = ""
        for i in range(len(classes)):
            if Lconfiance[i] == 0: continue
            confiance += '{} {}\n'.format(classes[i], Lconfiance[i])
        confiance+="=========================================="
        print(confiance)
    
    def predict_proba(self,x):
        x = np.asarray(x)        
        return self.model.predict_proba(self.transform(x))

# Add data
# rows, impossible transition with label "No"
def getNo(X,Y, max_n, ratio = 0.8):
    c = X.shape[1]//2
    X = X.astype(int)
    newX = X
    coupe_n = int(len(newX)*ratio)
    etatInital = np.unique(newX[:,:c], axis=0)[:coupe_n]
    L = [] # list of added rows
    i = 0 # number of added rows
    for e in etatInital: 
        # indices des etats impossibles depuis l'état e
        #indices = np.random.choice(np.where(e != X[:,:c])[0], 3, replace=False)
        indices = np.where(e != X[:,:c])[0][:]
        if len(indices) == 0: continue
        # On supprime les duplicatas
        etatFinal = np.unique(X[:,c:][indices], axis=0)
        print("etatFinal", len(etatFinal))
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
    X, Y = getData("data/data.csv")  
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

def testRaccourci(ratio = 0.2, print_score = False, render = False):
    X, Y = getData("data/data.csv") # Load data
    Y = np.array(["Yes"]*len(Y)) # transform label
    X,Y = getNobis(X,Y, len(Y)) # generate false data
    Xtrain, Ytrain, Xtest, Ytest = split(X, Y)

    # Classifier
    cf = MLPtrick()
    cf.fit(Xtrain,Ytrain)
    if print_score:
        getScore(cf,  Xtrain, Ytrain, Xtest, Ytest)
    if render:
        x = cf.transform(X)
        y = Y
        plot_frontiere_proba(cf.transform(X)[:,:2], lambda x: cf.model.predict_proba(np.hstack((x, np.zeros((len(x),1)))))[: ,0] ,step=50)
        plt.scatter(x[y=="No"][:,0], x[y=="No"][:,1], marker="x")
        plt.scatter(x[y=="Yes"][:,0], x[y=="Yes"][:,1], marker="o")
        plt.show()
    return cf

def calculeTemps():
    X, Y = getData("data/data.csv") # Load data
    classifieur = test()
    testeur = testRaccourci()
    n, d = X.shape
    Ltemps = []
    for x in X:
        start = time()
        testeur.predict([x])
        classifieur.predict([x])
        Ltemps.append(time() - start)
    Ltemps = np.array(Ltemps)*1e3
    plt.xlabel("indice des exemples")
    plt.ylabel("Temps en ms")
    print("\n=======  Temps de prédiction en ms ======")
    print("Min et Max: ", Ltemps.min(), Ltemps.max())
    print("Moyenne: ", np.mean(Ltemps))
    # plt.show()

    
    


if __name__=="__main__":
    calculeTemps()
    #testRaccourci(print_score = True, render=True)