from sklearn.tree import export_graphviz
from sklearn.tree import DecisionTreeClassifier as DTree
#import pydotplus
import numpy as np
import sklearn.linear_model.Perceptron


def makeExs(nbex,commandes):
    tirages = np.random.randint(0,100, nbex)

    exemples = []
    for e in tirages:
        # format sklearn a verifier (states, label)
        # Pour une approche tres simplifiee :
        # e = nombre de rectangles, e + 1 = nombre de rectangles + 1, label = numero de la liste de commandes
        exemples.append(( [e, e+1, np.random.randint(0,len(listecommandes)) ] ))
    
    return np.array(exemples)

def getData():
    


if __name__=="__main__":

    """
       Avec des données générées aléatoirement et 2 classes de commandes
       Il faut noter que les données étant aléatoire, c'est pas très représentatif des données
       la liste des commandes seront représenter par un chiffre pour simplifier l'apprentissage
       supervisé.
    """
    
    listecommandes = np.array([["dupliquer"],["copier","coller"]],dtype=object)

    exs = makeExs(5000,listecommandes)
    datax, datay = exs[:,:2], exs[:,2:]
    #print(" HERE",datax.shape,datay.shape)

    size = int(0.8*len(datax))
    dtrain, dtest = datax[:size], datax[size:]
    

    # On attribue un chiffre à chaque label, on fera une classification binaire pour l'instant
    labs = np.where(datay < 1, -1, 1)

    ytrain, ytest = labs[:size], labs[size:]
    #print("labs ",np.unique(labs))
    
    # Il faudra faire une base temporaire pour tester
    # On utilise SKLEARN pour avoir des modeles deja fait (reseau de neurones avec pytorch ?)
    # id2genre = [ x[1] for x in sorted (fields.items())[: -2]]
    dt = DTree ()
    dt.max_depth = 5 # on fixe la taille max de l’arbre a 5
    dt.min_samples_split = 2 # nombre minimum d ’ exemples pour spliter un noeud
    dt.fit ( dtrain , ytrain )
    dt.predict( dtrain [:5 ,:])

    # Pour l'instant il ne faut pas s'attendre a une performance tres bonne puisqu'on a pas de donnees reelles
    print ("Performance a l'apprentissage", dt.score( dtrain , ytrain ))
    print ( "Performance au test ",dt.score( dtest , ytest ))


    clf = Nn(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5, 2), random_state=1)
    clf.fit(dtrain,ytrain.T[0])

    print ("Performance a l'apprentissage", clf.score( dtrain , ytrain ))
    print ( "Performance au test ",clf.score( dtest , ytest ))
    
    # On pourrait par exemple donner des états et essayer ici de savoir quel commande sera donnée en
    # sortie, pour le cas de multi label, on utilisera la principe de 1 contre tous
