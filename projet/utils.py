import numpy as np
import pandas as pd

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