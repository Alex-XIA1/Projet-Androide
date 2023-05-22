import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mltools import plot_data, plot_frontiere, make_grid, gen_arti
from random import sample

# Extrait les données d'un fichier csv, en data et label
def getData(filename, remove_duplicata = True):
    with open(filename) as f:
        df = pd.read_csv(f)
        if remove_duplicata:
            df = df.drop_duplicates()
        X = df.to_numpy()
    return X[:,:-1], X[:,-1]

# Separe les données en données d'apprentissage et de test
def split(X, Y, ratio=0.8):
    n,d = X.shape
    indices = np.random.permutation(n)
    n_coupe = int(n*ratio)
    X = X[indices]
    Y = Y[indices]
    Xtrain, Ytrain = X[:n_coupe], Y[:n_coupe]
    Xtest, Ytest = X[n_coupe:], Y[n_coupe:]
    return Xtrain, Ytrain, Xtest, Ytest

# Transforme une matrice en une liste 1D
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

# Affiche le nombre d'occurence de chaque valeur
def show_counts(data, text = "Counts"):
    V,C = np.unique(data, return_counts = True)
    print("\n========= %s ==========" %text)
    print(" Value  |  Counts")
    for i in range(len(C)):
        print(V[i], '  -  ', C[i])
    print("==================================")


# Affiche toutes les infos sur les scores
def getScore(model, Xtrain, Ytrain, Xtest, Ytest, render = True):
    print("========================== Infos Scores =================================")
    prediction = model.predict(Xtest) # prediction sur les tests
    if render: # affiche les proportions des etiquettes de Ytrain et Ytests
        show_counts(Ytrain, "Train Stats") 
        show_counts(Ytest, "Test Stats")
    print("\n============== score: ===================")
    print("Paramters: train (%d), test(%d)" % (len(Ytrain), len(Ytest)))
    print("train: ", model.score(Xtrain,Ytrain))
    print("test: ", model.score(Xtest,Ytest))
    for y in np.unique(Ytest):
        indices = Ytest == y
        print("Y: ", y, " - ", model.score(Xtest[indices],Ytest[indices]))
        v,c = np.unique(prediction[indices][prediction[indices]!=y], return_counts=True)
        for i in range(len(v)):
            print("\t",v[i], " - ", c[i])
        print()

def plot_frontiere_proba(data,f,step=20):
    grid ,x,y = make_grid(data=data,step=step)
    plt.contourf (x , y , f(grid).reshape(x.shape) ,255)


def getNobis(X,Y, max_n, ratio = 0.8):
    L = []
    c = X.shape[1]//2
    G, D, etats = createGraph(X)
    cpt = 0
    for index in np.unique(G[:,0]):
        #print("I: ", index, " size: ", cpt)
        etatFinal = getStateInRange(index, D)
        #print("atteint: ", len(etatFinal))
        if len(etatFinal) == 0: continue
        #etatFinal = sample(etatFinal, 10)
        for i in etatFinal:
            L.append(np.hstack((etats[index],etats[i])))
            cpt+=1
            if cpt > max_n:
                break
        if cpt > max_n:
            break
    
    L = np.array(L)
    print("Generate %d data" %cpt)
    print("NoShape: ", L.shape)
    return np.concatenate((X, L), axis = 0), np.concatenate((Y, ["No"]*cpt), axis = 0)

def createGraph(X):
    print("Create Graph")
    n, d = X.shape
    c = X.shape[1]//2
    X = X.astype(int)
    etats = np.unique(np.vstack((X[:,:c],X[:,c:])), axis=0)
    G = np.zeros((n,2), dtype=int)
    D = dict()
    
    m = 0
    for i in range(len(etats)):
        m = max(len(getIndex(etats[i], X[:,:c])), m)
        G[getIndex(etats[i], X[:,:c]),0] = i
        G[getIndex(etats[i], X[:,c:]),1] = i

    for i in range(len(etats)):
        D[i] = set(G[G[:,0]==i,1])

    M = np.array([len(D[i]) for i in range(len(etats)) ])
    return G, D, etats

def getStateInRange(index, D, distance=5):
    voisins = D[index]
    Ouvert = set()
    Ferme = set()
   
    for i in voisins:
        Ouvert = Ouvert | D[i]
    voisins.add(index)
    Ouvert = Ouvert - voisins
    Ferme = Ferme | Ouvert
    for _ in range(distance-2):
        R = set()
        for i in Ouvert:
            R = R | D[i] 
        Ouvert = R - voisins - Ferme # nouveau elements sauf voisins et deja visite
        Ferme = Ferme | Ouvert
    return list(Ferme)

def getIndex(elt, L):
    return np.where(~(L - elt).any(axis=1))[0]


        
        
        
        
        
        



